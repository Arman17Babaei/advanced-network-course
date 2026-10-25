#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
year=2023
url=f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
soup=BeautifulSoup(requests.get(url,timeout=40,headers=H).text,"html.parser")

def norm(s): return " ".join(str(s).replace("\xa0"," ").split()).strip(" .")

def parse(li):
    box=li.find("p") or li
    out=[]; cur=None
    for node in box.children:
        name=getattr(node,"name",None)
        if name=="em":
            t=norm(node.get_text(" ",strip=True))
            if cur is None or cur["authors"]:
                cur={"title":t,"authors":""}; out.append(cur)
            else:
                cur["title"]=norm(cur["title"]+" "+t)
        elif name=="br": continue
        else:
            txt=norm(node.get_text(" ",strip=True) if hasattr(node,"get_text") else str(node))
            if txt and cur is not None: cur["authors"]=norm(cur["authors"]+" "+txt)
    return out

papers=[]
for tr in soup.find_all("tr"):
    cells=tr.find_all("td",recursive=False)
    if len(cells)<2: continue
    label=norm(cells[0].get_text(" ",strip=True)).lower()
    if "parallel technical" not in label and "best paper" not in label: continue
    for li in cells[1].find_all("li"):
        for p in parse(li):
            papers.append((label,p,li))

print(f"RAW={len(papers)} BLANK_AUTHORS={sum(not p[1]['authors'] for p in papers)}",flush=True)
for label,p,li in papers:
    if not p["authors"]:
        print(f"BLANK | {p['title']} | ROW={label}",flush=True)
        print("LI="+str(li)[:7000].replace("\n"," "),flush=True)
        nxt=li.find_next_sibling()
        print("NEXT="+(str(nxt)[:3000].replace("\n"," ") if nxt else "NONE"),flush=True)
        parent=li.parent
        print("PARENT="+str(parent)[:10000].replace("\n"," "),flush=True)
