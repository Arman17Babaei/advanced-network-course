#!/usr/bin/env python3
import difflib, re, requests
from bs4 import BeautifulSoup
H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
url="https://ssl.linklings.net/conferences/ipdps/ipdps2025_program/views/at_a_glance.html"
soup=BeautifulSoup(requests.get(url,timeout=40,headers=H).text,"html.parser")
best=[]; tech=[]
for sess in soup.select(".program-session"):
    st=sess.select_one(".session-title")
    sname=" ".join(st.stripped_strings) if st else "(none)"
    for slot in sess.select(".slot-wrapper"):
        cal=slot.select_one("a.calendar-link[href*='--pap']")
        title_tag=slot.select_one("span.ttip_object_info")
        if cal is None or title_tag is None: continue
        title=" ".join(title_tag.stripped_strings)
        if sname.strip()=="Best Paper Nominees": best.append(title)
        elif re.match(r"^\s*\d+\.",sname): tech.append(title)

def norm(s):
    s=s.lower()
    s=re.sub(r"[^a-z0-9]+"," ",s)
    return " ".join(s.split())

print(f"TECH={len(tech)} BEST={len(best)}",flush=True)
for b in best:
    scored=sorted(((difflib.SequenceMatcher(None,norm(b),norm(t)).ratio(),t) for t in tech),reverse=True)
    print("BEST | "+b,flush=True)
    for score,t in scored[:5]:
        print(f"  MATCH {score:.4f} | {t}",flush=True)
