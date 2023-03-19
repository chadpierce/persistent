'''
prompt:
modify this python script to add a beacon rating for each IP pair similar to how the RITA tool by active countermeasures analyzes data
'''

import csv
from collections import defaultdict
from datetime import datetime, timedelta
import sys

input_file = sys.argv[1]
chunk_size = timedelta(minutes=60)
output_rows = 10

timestamp_col = 0
source_ip_col = 1
dest_ip_col = 2

def get_chunk(timestamp):
    dt = datetime.strptime(timestamp, '%Y-%m-%d-%H:%M:%S')
    return dt - (dt - datetime.min) % chunk_size

with open(input_file) as f:
    reader = csv.reader(f)
    #next(reader) # skip header row
    counts = defaultdict(set)
    total_counts = defaultdict(int)
    for row in reader:
        timestamp, source_ip, dest_ip = row[timestamp_col], row[source_ip_col], row[dest_ip_col]
        chunk = get_chunk(timestamp)
        counts[(source_ip, dest_ip)].add(chunk)
        total_counts[(source_ip, dest_ip)] += 1

sorted_counts = sorted(counts.items(), key=lambda x: len(x[1]), reverse=True)

for pair, chunks in sorted_counts:
    beacon_rating = len(chunks) / total_counts[pair]
    print(f'{len(chunks)} - {total_counts[pair]} - {beacon_rating:.2f} - {pair[0]},{pair[1]}')