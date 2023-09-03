import requests
from bs4 import BeautifulSoup
import re

main_url = "https://crt.sh:443/?q=flipkart.com"
main_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://crt.sh/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
r=requests.get(main_url, headers=main_headers)
soup=BeautifulSoup(r.content,'html5lib')
urls=[]
for links in soup.find_all(text=re.compile("flipkart.com")):
    if(links[0]!="*"):
        print(links)

