import requests
from bs4 import BeautifulSoup
import re

main_url1 = "https://crt.sh:443/?q=flipkart.com"
main_headers1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://crt.sh/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
r1=requests.get(main_url1, headers=main_headers1)
soup1=BeautifulSoup(r1.content,'html5lib')
urls1=[]
for links in soup1.find_all(text=re.compile("flipkart.com")):
    if(links[0]!="*"):
        print(links)
main_url2 = "https://subdomainfinder.c99.nl/scans/2023-12-11/flipkart.com"
main_headers2 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://crt.sh/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
r2=requests.get(main_url2, headers=main_headers2)
soup2=BeautifulSoup(r2.content,'html5lib')
urls2=[]
for links in soup2.find_all(text=re.compile("flipkart.com")):
    if(links!="More scans of flipkart.com"):
        print(links)
    else:
        break
