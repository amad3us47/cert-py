def scrape_subdomainfinderc99():
    urls=f"https://subdomainfinder.c99.nl/scans/{target_domain}"
    headers={"Content-Type": "text"}
    r=requests.get(urls,header=headers)
    soup=BeautifulSoup(r.content,'html5lib')
    urls=[]

    for links in soup.find_all(string=re.compile(target_domain)):
        if(links[0] != "*"):
            return links
