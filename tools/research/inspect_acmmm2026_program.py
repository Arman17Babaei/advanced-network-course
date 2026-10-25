#!/usr/bin/env python3
import requests
url="https://2026.acmmm.org/site/technical-programme.html"
r=requests.get(url,timeout=60,headers={"User-Agent":"advanced-network-course/1.0"})
r.raise_for_status()
print("STATUS",r.status_code,"BYTES",len(r.content),"CT",r.headers.get("content-type"))
print(r.text)
