import requests
from bs4 import BeautifulSoup
import re
import argparse

def scrape_domain(target_domain):
    main_url1 = f"https://crt.sh:443/?q={target_domain}"
    main_headers1 = {"Content-Type": "text"}
    r1 = requests.get(main_url1, headers=main_headers1)
    soup1 = BeautifulSoup(r1.content, 'html5lib')
    urls1 = []

    for links in soup1.find_all(string=re.compile(target_domain)):
        if(links[0] != "*"):
            print(links)

    main_url2 = f"https://subdomainfinder.c99.nl/scans/{target_domain}"
    main_headers2 = {"Content-Type": "text"}
    r2 = requests.get(main_url2, headers=main_headers2)
    soup2 = BeautifulSoup(r2.content, 'html5lib')
    urls2 = []

    for links in soup2.find_all(string=re.compile(target_domain)):
        if(links != f"More scans of {target_domain}"):
            print(links)
        else:
            break

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Scrape URLs for a given domain.")
    parser.add_argument("-d", "--domain", type=str, help="Target domain to scrape")
    args = parser.parse_args()

    if args.domain:
        scrape_domain(args.domain)
    else:
        print("Please provide a target domain using the -d or --domain option.")
