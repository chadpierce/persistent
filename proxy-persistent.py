#!/usr/bin/env python3

# THIS SCRIPT IS PROVIDED "AS IS" WITH NO WARRANTIES OR GUARANTEES OF ANY
# KIND, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE. ALL RISKS OF DAMAGE REMAINS WITH THE USER, EVEN IF THE
# AUTHOR, SUPPLIER OR DISTRIBUTOR HAS BEEN ADVISED OF THE POSSIBILITY OF ANY
# SUCH DAMAGE. IF YOUR STATE DOES NOT PERMIT THE COMPLETE LIMITATION OF
# LIABILITY, THEN DO NOT DOWNLOAD OR USE THE SCRIPT. NO TECHNICAL SUPPORT
# WILL BE PROVIDED.
#
# proxy-persistent.py 
# BASED ON: persistent.pl, written by Eric Conrad
# PORTED BY: Bing Chat
#
# usage: Usage: python script.py <filename>
#
# Reports persistent http connections via the proxy, where a client
# persistently connects to the same site over a long duration of time.
#
# May identify reverse http proxies, and worms/trojans that 'phone home' 
# on a regular basis
# 
# May also identify legitimate persistent connections, such as weather 
# toolbars, streaming media, etc.  Expect false positives.
# 
# Best to scan on 'off-hours' traffic (late night to early morning)
#
# output is client -> server pairs, sorted by number of connections
#
# Assumes squid proxy log format with "emulate_httpd_log" set to "on"
# Here's an example of GET and CONNECT entries:
#
# 172.23.102.26 - - [02/Apr/2007:14:25:06 -0400] "GET http://img.mqcdn.com/mapquest/brands/mqsite/promos-min.css?v=1.191 HTTP/1.0" 200 3812 TCP_MISS:DIRECT
# 172.22.116.210 - - [19/May/2007:06:30:02 -0400] "CONNECT telrad.mobilexusa.com:443 HTTP/1.0" 200 1010 TCP_MISS:DIRECT

import sys

if len(sys.argv) != 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

numbertoreport = 50
lastmin = 0
min = 0
url = ""
urlfields = []
datefields = []
client = ""
date = ""
site = ""
logline = []
connection = ""
seen = {}
persistent = {}
key = ""

with open(filename) as f:
    for line in f:
        if " \"CONNECT " in line or "GET http://" in line:
            logline=line.split()
            client=logline[0]
            date=logline[3]
            if " \"CONNECT " in line:
                site=logline[6]
            else:
                url=logline[6]
                urlfields=url.split("/")
                site=urlfields[2]
            connection=client + " " + site
            seen[connection]=1
            datefields=date.split(":")
            min=int(datefields[2])
            if min % 5 == 0 and min != lastmin:
                lastmin=min
                for key in seen.keys():
                    if key not in persistent:
                        persistent[key] = 0
                    persistent[key] += seen[key]
                    seen[key]=0

keys=sorted(persistent.keys(), key=lambda x: persistent[x], reverse=True)

for key in keys[:numbertoreport]:
    # print(key + ": " + str(persistent[key]))  # AI's orig output
    print(str(persistent[key]) + " - " + key)