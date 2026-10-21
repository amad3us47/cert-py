
import csv
import json
import os
import time
from pathlib import Path

import requests

DOMAIN = "amazon.com"
API = "https://api.certspotter.com/v1/issuances"

CHECKPOINT = Path("certspotter_checkpoint.json")
OUTPUT = Path("certspotter_history.csv")
API_KEY = os.getenv("CERTSPOTTER_API_KEY")

params = [
    ("domain", DOMAIN),
    ("include_subdomains", "true"),
    ("expand", "dns_names"),
]

session = requests.Session()
session.headers["User-Agent"] = "PersonalCTResearch/1.0"

if API_KEY:
    session.headers["Authorization"] = f"Bearer {API_KEY}"

fields = ["certificate_id", "not_before", "not_after", "domain"]

if CHECKPOINT.exists():
    state = json.loads(CHECKPOINT.read_text())
    after = state.get("after")
    print("Resuming after certificate:", after)
else:
    after = None

# Create the output file if needed
if not OUTPUT.exists():
    with OUTPUT.open("w", newline="") as f:
        csv.DictWriter(f, fieldnames=fields).writeheader()

page = 0
backoff = 60

while True:
    query = params.copy()
    if after:
        query.append(("after", after))

    try:
        response = session.get(API, params=query, timeout=60)

        if response.status_code == 429:
            wait = response.headers.get("Retry-After")
            try:
                wait = max(1, int(wait)) if wait else backoff
            except ValueError:
                wait = backoff

            print(f"Rate limited. Waiting {wait}s...")
            time.sleep(wait)
            backoff = min(backoff * 2, 1800)
            continue

        response.raise_for_status()
        batch = response.json()
        backoff = 60

        if not batch:
            print("API returned no more records.")
            break

        # Append the complete page before advancing the checkpoint
        with OUTPUT.open("a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)

            for cert in batch:
                for name in cert.get("dns_names", []):
                    name = name.lower().rstrip(".")
                    if name.startswith("*."):
                        name = name[2:]

                    if name == DOMAIN or name.endswith("." + DOMAIN):
                        writer.writerow({
                            "certificate_id": cert.get("id", ""),
                            "not_before": cert.get("not_before", ""),
                            "not_after": cert.get("not_after", ""),
                            "domain": name,
                        })

        after = batch[-1]["id"]
        CHECKPOINT.write_text(json.dumps({"after": after}))
        page += 1

        print(f"Page {page}: {len(batch)} certificates saved.")

    except KeyboardInterrupt:
        print("\nStopped. Progress is saved; rerun to resume.")
        break
    except requests.RequestException as e:
        print("Request failed:", e)
        print("Checkpoint preserved. Rerun later to resume.")
        break

print("CSV:", OUTPUT.resolve())
print("Checkpoint:", CHECKPOINT.resolve())

