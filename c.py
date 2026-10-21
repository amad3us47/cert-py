
import requests
import json

API = (
    "https://windvane.lichoin.com/"
    "trpc.backendhub.public.WindvaneService/ListSubDomain"
)

DOMAIN = "google.com"  # Replace with your target
API_KEY = "YOUR_API_KEY"  # Use your Windvane API key

response = requests.post(
    API,
    headers={
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY,
    },
    json={
        "domain": DOMAIN,
        "page_request": {
            "page": 1,
            "count": 1000,
        },
    },
    timeout=30,
)

print("HTTP:", response.status_code)

try:
    data = response.json()
    print(json.dumps(data, indent=2)[:10000])

    # Extract domains if the expected response structure is present
    entries = data.get("data", {}).get("list", [])
    domains = sorted({
        entry["domain"]
        for entry in entries
        if entry.get("domain")
    })

    print("\nDomains found:", len(domains))
    for domain in domains:
        print(domain)

except ValueError:
    print(response.text[:2000])

