def scrape_certspotter(target_domain):

    url = "https://api.certspotter.com/v1/issuances"

    params = {
        "domain": target_domain,
        "include_subdomains": "true",
        "expand": "dns_names"
    }

    headers = {
        "User-Agent": "PersonalCTResearch/1.0"
    }

    api_key = os.getenv("CERTSPOTTER_API_KEY")

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    subdomains = set()
    after = None
    backoff = 60

    while True:

        query = params.copy()

        if after:
            query["after"] = after

        try:
            response = requests.get(
                url,
                params=query,
                headers=headers,
                timeout=60
            )

            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", backoff))
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                backoff = min(backoff * 2, 1800)
                continue

            response.raise_for_status()

            rows = response.json()
            backoff = 60

            if not rows:
                break

            for cert in rows:
                for name in cert.get("dns_names", []):

                    host = name.lower().rstrip(".")

                    if host.startswith("*."):
                        host = host[2:]

                    if host == target_domain or host.endswith("." + target_domain):
                        subdomains.add(host)

            after = rows[-1]["id"]

            print(f"Collected {len(subdomains)} unique hostnames")

        except requests.RequestException as e:
            print("Request failed:", e)
            break

    return sorted(subdomains)
