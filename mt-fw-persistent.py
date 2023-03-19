import sys
from threading import Thread

if len(sys.argv) != 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

# file format (split by comma)
filename = sys.argv[1]
indexTimestamp = 0
indexSourceIP = 1
indexDestIP = 2

chunkInterval = 1
numbertoreport = 50
lastmin = 0
min = 0

seen = {}
persistent = {}

def process_line(line):
    global lastmin
    logline=line.split(',')
    
    if len(logline) < max(indexSourceIP,indexDestIP)+1:
        return
    
    client=logline[indexSourceIP]
    date=logline[indexTimestamp]
    dest=logline[indexDestIP]
    connection=client + " " + dest
    seen[connection]=1
    min=int(date.split(":")[1]) # minutes field
    
    if min % chunkInterval == 0 and min != lastmin:
        lastmin=min
        
        for key in seen.keys():
            if key not in persistent:
                persistent[key] = 0
                
            persistent[key] += seen[key]
            seen[key]=0

with open(filename) as f:
    threads=[]
    
    for line in f:
        t=Thread(target=process_line,args=(line,))
        t.start()
        threads.append(t)
        
for t in threads:
    t.join()

keys=sorted(persistent.keys(), key=lambda x: persistent[x], reverse=True)

for key in keys[:numbertoreport]:
    print(str(persistent[key]) + " - " + key)