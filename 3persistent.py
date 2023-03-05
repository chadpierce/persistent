'''
prompt 1:
write a python script that takes a csv file as input. the csv file has 5 columns (timestamp, source_ip, dest_ip, bytes_sent, bytes_received). the source_ip and dest_ip columns are IP addresses that represent connections between 2 devices. the script should create a list of IP address pairs, and then count how many chunks each IP pair appears in. the script should then output the number of 5 minute chunks each IP appears in, in descending order by chunk count. do this is the most efficient way possible. 

input file should be accepted as a command line argument
the number of rows in the output should be configurable and set as a variable
the 5 minute interval should set as a variable and configurabled

example of the csv format is below:
2023-03-03 18:54:10 UTC,10.156.345.59,65.122.40.566,511,704

prompt2:
the output shows how many rows each ip pair appears in. the output should show how many 5 minute chunks each ip pair appears in. please fix

prompt3:
are you able to refactor this program to make it more time efficient

the chatbot responded:
The current version of the script should already be quite efficient for most input files. It reads the input file once and processes each row in constant time. The sorting step at the end takes O(n log n) time, where n is the number of unique IP pairs. 

It then proceeded to provide suggestions such as sorting the input file by time beforehand. 
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

with open(input_file) as f:
    reader = csv.reader(f)
    next(reader) # skip header row
    counts = defaultdict(set)
    for row in reader:
        timestamp, source_ip, dest_ip, _, _ = row
        chunk = get_chunk(timestamp)
        counts[(source_ip, dest_ip)].add(chunk)

sorted_counts = sorted(counts.items(), key=lambda x: len(x[1]), reverse=True)

for pair, chunks in sorted_counts[:output_rows]:
    #print(f'{pair[0]} <-> {pair[1]}: {len(chunks)}')  # chatbot's output format
    print(f'{len(chunks)} - {pair[0]},{pair[1]}')