
import requests
from urllib.parse import urlparse

domain = "example.com"  # Replace with your target

url = "https://web.archive.org/cdx/search/cdx"
params = {
    "url": f"*.{domain}/*",
    "output": "json",
    "collapse": "urlkey",
    "fl": "original",
}

response = requests.get(url, params=params, timeout=60)
print("HTTP:", response.status_code)
response.raise_for_status()

rows = response.json()
subdomains = set()

for row in rows[1:]:  # Skip header
    archived_url = row[0]
    host = (urlparse(archived_url).hostname or "").lower()

    if host == domain or host.endswith("." + domain):
        subdomains.add(host)

with open("wayback_subdomains.txt", "w") as f:
    f.write("\n".join(sorted(subdomains)) + "\n")

print(f"Found {len(subdomains)} unique hostnames")
print("Saved to wayback_subdomains.txt")

for host in sorted(subdomains):
    print(host)

