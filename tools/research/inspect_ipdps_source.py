#!/usr/bin/env python3
import collections, requests, re
from bs4 import BeautifulSoup
H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
url="https://ssl.linklings.net/conferences/ipdps/ipdps2025_program/views/at_a_glance.html"
soup=BeautifulSoup(requests.get(url,timeout=40,headers=H).text,"html.parser")
sessions=collections.defaultdict(list)
allrows=[]
for sess in soup.select(".program-session"):
    st=sess.select_one(".session-title")
    sname=" ".join(st.stripped_strings) if st else "(none)"
    for slot in sess.select(".slot-wrapper"):
        cal=slot.select_one("a.calendar-link[href*='--pap']")
        title_tag=slot.select_one("span.ttip_object_info")
        authors=slot.select_one(".author-names")
        if cal is None or title_tag is None or authors is None: continue
        title=" ".join(title_tag.stripped_strings)
        href=cal.get("href","")
        sessions[sname].append((title,href))
        allrows.append((title,sname,href))
print(f"PAP_SLOTS={len(allrows)} UNIQUE_TITLES={len({x[0] for x in allrows})}",flush=True)
for s,vals in sessions.items():
    print(f"SESSION | {s} | count={len(vals)}",flush=True)
    if not re.match(r"^\s*\d+\.",s):
        for t,h in vals:
            print(f"  NONTECH | {t} | {h}",flush=True)
# duplicates by title
cnt=collections.Counter(t for t,_,_ in allrows)
print("DUPLICATES",flush=True)
for t,n in cnt.items():
    if n>1:
        print(f"  {n}x | {t}",flush=True)
