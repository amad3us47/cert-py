import requests
from bs4 import BeautifulSoup
import re

main_url = "https://crt.sh:443/?q=flipkart.com"
main_headers = {"Content-Type":"text"}
r=requests.get(main_url, headers=main_headers)
soup=BeautifulSoup(r.content,'html5lib')
urls=[]
for links in soup.find_all(text=re.compile("flipkart.com")):
    if(links[0]!="*"):
        print(links)

