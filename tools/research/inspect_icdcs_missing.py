#!/usr/bin/env python3
import requests, re
from bs4 import BeautifulSoup

H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
sources={
  2024:"https://icdcs2024.icdcs.org/accepted-papers/",
  2025:"https://icdcs2025.icdcs.org/accepted-papers/",
  2026:"https://icdcs2026.icdcs.org/program/main-technical-sessions/",
}
for year,url in sources.items():
    r=requests.get(url,timeout=45,headers=H)
    print(f"YEAR={year} STATUS={r.status_code} URL={r.url} BYTES={len(r.content)}",flush=True)
    r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    print("HEADINGS",flush=True)
    for h in soup.find_all(["h1","h2","h3","h4","h5"]):
        txt=" ".join(h.stripped_strings)
        if txt:
            print(f"  {h.name} | {txt[:500]}",flush=True)

    if year in (2024,2025):
        target_pat="regular submission" if year==2024 else "main track"
        main=None
        for h in soup.find_all(["h1","h2","h3","h4"]):
            if target_pat in " ".join(h.stripped_strings).lower():
                main=h; break
        print("MAIN="+(" ".join(main.stripped_strings) if main else "NONE"),flush=True)
        if main:
            cur=main.find_next_sibling()
            i=0
            while cur is not None and i<10:
                if cur.name in ["h1","h2","h3","h4"]:
                    print("NEXT_HEADING="+" ".join(cur.stripped_strings),flush=True)
                    break
                txt=" ".join(cur.stripped_strings) if hasattr(cur,"stripped_strings") else ""
                if txt:
                    print(f"BLOCK {cur.name} | {txt[:1800]}",flush=True)
                    print("MARKUP="+str(cur)[:7000].replace("\n"," "),flush=True)
                cur=cur.find_next_sibling(); i+=1
        print(f"TABLES={len(soup.find_all('table'))} TR={len(soup.find_all('tr'))} P={len(soup.find_all('p'))}",flush=True)

    if year==2026:
        # WordPress renders technical rows as table rows; inspect rows containing paper IDs.
        candidates=[]
        for tr in soup.find_all("tr"):
            cells=[" ".join(td.stripped_strings) for td in tr.find_all(["td","th"])]
            if len(cells)>=3 and re.match(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}$",cells[0]) and cells[1].isdigit():
                candidates.append((tr,cells))
        print(f"PAPER_ROWS={len(candidates)}",flush=True)
        for tr,cells in candidates[:8]:
            print("ROW="+repr(cells),flush=True)
            print("MARKUP="+str(tr)[:3500].replace("\n"," "),flush=True)
        print(f"TABLES={len(soup.find_all('table'))} TR={len(soup.find_all('tr'))}",flush=True)
    print("----",flush=True)
