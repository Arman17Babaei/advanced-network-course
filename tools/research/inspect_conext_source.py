#!/usr/bin/env python3
import re
import requests

for year in [2023,2024,2025,2026]:
    base=f"https://conferences2.sigcomm.org/co-next/{year}/"
    r=requests.get(base,timeout=10,headers={"User-Agent":"advanced-network-course-source-inspector/1.0"})
    print(f"YEAR={year} STATUS={r.status_code} BYTES={len(r.content)}", flush=True)
    raw=r.text
    low=raw.lower()
    for term in ["accepted", "program", "papers"]:
        print(f"TERM={term} occurrences={low.count(term)}", flush=True)
        for m in list(re.finditer(term, low))[:10]:
            a=max(0,m.start()-180); b=min(len(raw),m.end()+260)
            snippet=re.sub(r"\s+"," ",raw[a:b])
            print("  "+snippet[:500], flush=True)
    urls=sorted(set(re.findall(r'''(?:href|src|url)\s*[=:]\s*["']([^"'#]+)["']''',raw,re.I)))
    for u in urls:
        if any(k in u.lower() for k in ["accept","program","paper"]):
            print(f"URL_CANDIDATE={u}", flush=True)
    print("----", flush=True)
