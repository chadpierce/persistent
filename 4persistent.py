'''
prompt: (based on version 3) please add another output after the IP pair that includes statistics on the bytes_sent and bytes_received data that may indicate c2 beacon traffic

response:
This version of the script keeps track of the bytes_sent and bytes_received values for each IP pair using two additional defaultdicts. After reading all the rows from the input file and adding each value to the appropriate list in sent_stats and recv_stats, the script sorts the counts by the number of unique chunks and prints out the top output_rows results along with statistics on the total and average number of bytes sent and received.

The get_stats function takes a list of values (either bytes_sent or bytes_received) and returns a string with statistics on those values. In this case it calculates the total and average number of bytes.

You can still change the number of rows in the output and size of each chunk by setting output_rows and chunk_size, respectively.
'''
import csv
from collections import defaultdict
from datetime import datetime, timedelta
import sys

input_file = sys.argv[1]
chunk_size = timedelta(minutes=5)
output_rows = 10

def get_chunk(timestamp):
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %Z')
    return dt - (dt - datetime.min) % chunk_size

def get_stats(values):
    values = list(map(int, values))
    total = sum(values)
    avg = total / len(values)
    return f'total: {total}, avg: {avg:.2f}'

with open(input_file) as f:
    reader = csv.reader(f)
    next(reader) # skip header row
    counts = defaultdict(set)
    sent_stats = defaultdict(list)
    recv_stats = defaultdict(list)
    for row in reader:
        timestamp, source_ip, dest_ip, bytes_sent, bytes_received = row
        chunk = get_chunk(timestamp)
        pair = (source_ip, dest_ip)
        counts[pair].add(chunk)
        sent_stats[pair].append(bytes_sent)
        recv_stats[pair].append(bytes_received)

sorted_counts = sorted(counts.items(), key=lambda x: len(x[1]), reverse=True)

for pair, chunks in sorted_counts[:output_rows]:
    sent_str = get_stats(sent_stats[pair])
    recv_str = get_stats(recv_stats[pair])
    #print(f'{pair[0]} <-> {pair[1]}: {len(chunks)}, sent: ({sent_str}), received: ({recv_str})')
    print(f'{len(chunks)} - {pair[0]},{pair[1]} - [out: ({sent_str}), in: ({recv_str})]')
