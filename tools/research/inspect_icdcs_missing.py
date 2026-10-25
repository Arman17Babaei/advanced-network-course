#!/usr/bin/env python3
import requests, re
from bs4 import BeautifulSoup

H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
sources={
  2023:"https://icdcs2023.icdcs.org/programs/",
  2024:"https://icdcs2024.icdcs.org/accepted-papers/",
  2025:"https://icdcs2025.icdcs.org/accepted-papers/",
  2026:"https://icdcs2026.icdcs.org/program/main-technical-sessions/",
}

for year,url in sources.items():
    r=requests.get(url,timeout=45,headers=H)
    print(f"YEAR={year} STATUS={r.status_code} URL={r.url} BYTES={len(r.content)}",flush=True)
    r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    print("TITLE="+(" ".join(soup.title.stripped_strings) if soup.title else ""),flush=True)

    headings=[]
    for h in soup.find_all(["h1","h2","h3","h4","h5"]):
        txt=" ".join(h.stripped_strings)
        if txt:
            headings.append((h.name,txt))
    print(f"HEADINGS={len(headings)}",flush=True)
    for x in headings[:80]:
        print(f"  H {x[0]} | {x[1][:300]}",flush=True)

    for tag in ["table","tr","li","p"]:
        els=soup.find_all(tag)
        print(f"TAG={tag} COUNT={len(els)}",flush=True)

    if year==2023:
        # Main session headings and the content immediately following them.
        shown=0
        for h in soup.find_all(["h2","h3","h4"]):
            txt=" ".join(h.stripped_strings)
            if re.match(r"Session\s+[ABC]-\d+",txt,re.I):
                print(f"SESSION={txt}",flush=True)
                sib=h.find_next_sibling()
                n=0
                while sib is not None and n<8:
                    if sib.name in ["h2","h3","h4"] and "Session" in " ".join(sib.stripped_strings):
                        break
                    st=" ".join(sib.stripped_strings) if hasattr(sib,"stripped_strings") else ""
                    if st:
                        print(f"  SIB {sib.name} | {st[:800]}",flush=True)
                        print(f"  MARKUP={str(sib)[:2200].replace(chr(10),' ')}",flush=True)
                    sib=sib.find_next_sibling(); n+=1
                shown+=1
                if shown>=4: break

    elif year in (2024,2025):
        # Identify heading boundaries and table/list rows near main track sections.
        main=None
        for h in soup.find_all(["h2","h3","h4"]):
            txt=" ".join(h.stripped_strings).lower()
            if (year==2024 and "regular submission" in txt) or (year==2025 and "main track" in txt):
                main=h; break
        print("MAIN_HEADING="+(" ".join(main.stripped_strings) if main else "NONE"),flush=True)
        if main:
            cur=main.find_next_sibling()
            n=0
            while cur is not None and n<12:
                if cur.name in ["h1","h2","h3","h4"] and cur is not main:
                    print("NEXT_HEADING="+" ".join(cur.stripped_strings),flush=True)
                    break
                txt=" ".join(cur.stripped_strings) if hasattr(cur,"stripped_strings") else ""
                if txt:
                    print(f"  BLOCK {cur.name} | {txt[:1200]}",flush=True)
                    print(f"  MARKUP={str(cur)[:3500].replace(chr(10),' ')}",flush=True)
                cur=cur.find_next_sibling(); n+=1

    elif year==2026:
        # The public page renders paper rows directly; inspect paragraph/table structure.
        candidates=[]
        for el in soup.find_all(["p","tr","li"]):
            txt=" ".join(el.stripped_strings)
            if re.match(r"\d{1,2}:\d{2}-\d{1,2}:\d{2}\s+\|\s+\d+\s+\|",txt):
                candidates.append(el)
        print(f"PAPER_CANDIDATES={len(candidates)}",flush=True)
        for el in candidates[:8]:
            print("  PAPER="+ " ".join(el.stripped_strings)[:1200],flush=True)
            print("  MARKUP="+str(el)[:2500].replace(chr(10)," "),flush=True)
    print("----",flush=True)
