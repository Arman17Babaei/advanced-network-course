#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
year=2023
url=f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
soup=BeautifulSoup(requests.get(url,timeout=40,headers=H).text,"html.parser")

def norm(s):
    return " ".join(str(s).replace("\xa0"," ").split()).strip(" .")

def papers_in_li(li):
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
        elif name=="br":
            continue
        else:
            txt=norm(node.get_text(" ",strip=True) if hasattr(node,"get_text") else str(node))
            if txt and cur is not None:
                cur["authors"]=norm(cur["authors"]+" "+txt)
    return out

tech=[]; best=[]
for tr in soup.find_all("tr"):
    cells=tr.find_all("td",recursive=False)
    if len(cells)<2: continue
    label=norm(cells[0].get_text(" ",strip=True)).lower()
    target=None
    if "parallel technical" in label: target=tech
    elif "best paper" in label: target=best
    if target is None: continue
    for li in cells[1].find_all("li"):
        target.extend(papers_in_li(li))

T={norm(x["title"]).lower():x for x in tech}
B={norm(x["title"]).lower():x for x in best}
print(f"TECH_RAW={len(tech)} TECH_UNIQUE={len(T)} BEST_RAW={len(best)} BEST_UNIQUE={len(B)}",flush=True)
print(f"INTERSECTION={len(set(T)&set(B))}",flush=True)
for k in sorted(set(T)&set(B)):
    print("OVERLAP | "+T[k]["title"],flush=True)
print("TECH_EXTRA_SPLITS:",flush=True)
for x in tech:
    if x["title"] in ["Exact Fault-Tolerant Consensus with Voting Validity","Smart Red Belly Blockchain: Reducing Congestion for Web3"]:
        print(f"  {x['title']} | {x['authors']}",flush=True)
print("BEST:",flush=True)
for x in best:
    print(f"  {x['title']} | {x['authors']}",flush=True)
