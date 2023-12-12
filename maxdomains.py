import requests
from bs4 import BeautifulSoup
import re

main_url1 = "https://crt.sh:443/?q=flipkart.com"}
main_headers1 = {"Content-Type":"text"}
r1=requests.get(main_url1, headers=main_headers1)
soup1=BeautifulSoup(r1.content,'html5lib')
urls1=[]
for links in soup1.find_all(text=re.compile("flipkart.com")):
    if(links[0]!="*"):
        print(links)
main_url2 = "https://subdomainfinder.c99.nl/scans/2023-12-11/flipkart.com"
main_headers2 = {"Content-Type":"text"}
r2=requests.get(main_url2, headers=main_headers2)
soup2=BeautifulSoup(r2.content,'html5lib')
urls2=[]
for links in soup2.find_all(text=re.compile("flipkart.com")):
    if(links!="More scans of flipkart.com"):
        print(links)
    else:
        break
