#!/usr/bin/env python3

# THIS SCRIPT IS PROVIDED "AS IS" WITH NO WARRANTIES OR GUARANTEES OF ANY
# KIND, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE. ALL RISKS OF DAMAGE REMAINS WITH THE USER, EVEN IF THE
# AUTHOR, SUPPLIER OR DISTRIBUTOR HAS BEEN ADVISED OF THE POSSIBILITY OF ANY
# SUCH DAMAGE. IF YOUR STATE DOES NOT PERMIT THE COMPLETE LIMITATION OF
# LIABILITY, THEN DO NOT DOWNLOAD OR USE THE SCRIPT. NO TECHNICAL SUPPORT
# WILL BE PROVIDED.
#
# fw-persistent.py
# BASED ON: persistent.pl, written by Eric Conrad
# PORTED BY: Bing Chat
# MODIFIED BY: Chad Pierce
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
# SAMPLE FIREWALL LOG FORMAT:
# 2023-03-03 18:50:28 UTC,10.0.329.52,65.124.136.145,737,808
# 2023-03-03 18:50:27 UTC,10.0.343.58,119.118.46.46,2973,714

import sys

if len(sys.argv) != 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

# file format (split by comma)
filename = sys.argv[1]
indexTimestamp = 0
indexSourceIP = 1
indexDestIP = 2
# TODO do something with bytes

chunkInterval = 1
numbertoreport = 50
lastmin = 0
min = 0
url = ""
urlfields = []
datefields = []
client = ""
date = ""
dest = ""
logline = []
connection = ""
seen = {}
persistent = {}
key = ""

with open(filename) as f:
    for line in f:
        logline=line.split(',')
        client=logline[indexSourceIP]
        date=logline[indexTimestamp]
        dest=logline[indexDestIP]
        connection=client + " " + dest
        seen[connection]=1
        min=int(date.split(":")[1])  # minutes field
        if min % chunkInterval == 0 and min != lastmin:
            lastmin=min
            for key in seen.keys():
                if key not in persistent:
                    persistent[key] = 0
                persistent[key] += seen[key]
                seen[key]=0

keys=sorted(persistent.keys(), key=lambda x: persistent[x], reverse=True)

for key in keys[:numbertoreport]:
    print(str(persistent[key]) + " - " + key)