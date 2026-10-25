#!/usr/bin/env python3
import re
import requests

H={"User-Agent":"advanced-network-course-source-inspector/1.0"}
for year in [2023,2024,2025,2026]:
    base=f"https://conferences2.sigcomm.org/co-next/{year}/"
    print(f"YEAR={year}",flush=True)
    for path in ["js/app.js","js/variables.js"]:
        url=base+path
        r=requests.get(url,timeout=15,headers=H)
        print(f"  FILE={path} STATUS={r.status_code} BYTES={len(r.content)}",flush=True)
        if r.status_code!=200:
            continue
        raw=r.text
        low=raw.lower()
        templates=sorted(set(re.findall(r'''templateUrl\s*:\s*["']([^"']+)["']''',raw,re.I)))
        for t in templates:
            if any(k in t.lower() for k in ["accept","program","paper"]):
                print(f"    TEMPLATE={t}",flush=True)
        for term in ["accepted","program","papers"]:
            positions=[m.start() for m in re.finditer(term,low)]
            print(f"    TERM={term} N={len(positions)}",flush=True)
            for pos in positions[:8]:
                snippet=re.sub(r"\s+"," ",raw[max(0,pos-260):min(len(raw),pos+520)])
                print("      "+snippet[:780],flush=True)
    print("----",flush=True)
