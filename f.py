
import requests
import csv
import time

DOMAIN = "amazon.com"
API = "https://api.certspotter.com/v1/issuances"

params = [
    ("domain", DOMAIN),
    ("include_subdomains", "true"),
    ("expand", "dns_names"),
]

session = requests.Session()
session.headers["User-Agent"] = "Historical-Certificate-Research/1.0"

seen = set()
rows = []
after = None

while True:
    query = params.copy()
    if after:
        query.append(("after", after))

    r = session.get(API, params=query, timeout=45)

    if r.status_code == 429:
        print("Rate limited. Stop and retry later.")
        break

    r.raise_for_status()
    batch = r.json()

    if not batch:
        print("No more results.")
        break

    for cert in batch:
        cert_id = cert.get("id")
        if not cert_id:
            continue

        for name in cert.get("dns_names", []):
            name = name.lower().removeprefix("*.")
            if name == DOMAIN or name.endswith("." + DOMAIN):
                key = (cert_id, name)
                if key not in seen:
                    seen.add(key)
                    rows.append({
                        "domain": name,
                        "not_before": cert.get("not_before", ""),
                        "not_after": cert.get("not_after", ""),
                        "certificate_id": cert_id,
                    })

    after = batch[-1]["id"]
    print(f"Fetched {len(batch)} certificates; {len(rows)} domain records")
    time.sleep(1)

with open("certspotter_history.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "domain", "not_before", "not_after", "certificate_id"
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

print("Saved certspotter_history.csv")

