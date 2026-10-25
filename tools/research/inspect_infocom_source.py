#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

H={"User-Agent":"Mozilla/5.0"}
hosts=["https://dblp.org","https://dblp1.uni-trier.de","https://dblp.uni-trier.de"]
for host in hosts:
    url=host+"/db/conf/infocom/infocom2026.html"
    try:
        r=requests.get(url,headers=H,timeout=30,allow_redirects=True)
    except Exception as e:
        print(f"HOST={host} ERROR={e}",flush=True); continue
    soup=BeautifulSoup(r.text,"html.parser")
    print(
        f"HOST={host} STATUS={r.status_code} FINAL={r.url} BYTES={len(r.content)} "
        f"TITLE={' '.join(soup.title.stripped_strings) if soup.title else ''!r} "
        f"ENTRY={len(soup.select('li.entry'))} TITLE_SPANS={len(soup.select('span.title'))}",
        flush=True,
    )
    for el in soup.select("li.entry")[:2]:
        print("  "+" ".join(el.stripped_strings)[:500],flush=True)
