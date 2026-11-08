def scrape_wayback(target_domain):

    urls = f"https://web.archive.org/cdx/search/cdx?url=*.{target_domain}/*&output=json&collapse=urlkey&fl=original"

    r = requests.get(urls, timeout=60)
    r.raise_for_status()

    rows = r.json()
    subdomains = set()

    for links in rows[1:]:
        host = (urlparse(links[0]).hostname or "").lower()

        if host == target_domain or host.endswith("." + target_domain):
            subdomains.add(host)

    return sorted(subdomains)
