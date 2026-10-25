#!/usr/bin/env python3
import requests
from urllib.parse import urlencode

u="https://dblp.org/search/publ/api"
params={"q":"toc:db/conf/ipps/ipdps2023.bht:","h":"1000","format":"json"}
r=requests.get(u,params=params,timeout=30,headers={"User-Agent":"advanced-network-course/1.0"})
print("URL",r.url)
print("STATUS",r.status_code)
print("CONTENT_TYPE",r.headers.get("content-type"))
print("BYTES",len(r.content))
print(r.text[:1200])
