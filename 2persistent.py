'''
write a python script that takes a csv file as input. the csv file has 5 columns (timestamp, source_ip, dest_ip, bytes_sent, bytes_received). the source_ip and dest_ip columns are IP addresses that represent connections between 2 devices. the script should create a list of IP address pairs, and then break the input log file into 5 minute chunks, and then count how many chunks each IP pair appears in. the script should then output the number of 5 minute chunks each IP appears in, in descending order by chunk count. 

input file should be accepted as a command line argument
the number of rows in the output should be configurable and stored as a variable
the 5 minute interval should be stored as a variable and configurable

example of the csv format is below:
2023-03-03 18:54:10 UTC,10.156.345.59,65.122.40.566,511,704

'''
import csv
from collections import defaultdict
from datetime import datetime, timedelta
import sys

def process_csv(file_name: str, interval: int = 5, output_rows: int = 10):
    with open(file_name) as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S %Z')
            source_ip = row[1]
            dest_ip = row[2]
            data.append((timestamp, source_ip, dest_ip))
    
    start_time = min([x[0] for x in data])
    end_time = max([x[0] for x in data])
    
    chunk_counts = defaultdict(int)
    
    current_time = start_time
    while current_time < end_time:
        next_time = current_time + timedelta(minutes=interval)
        chunk_data = [x for x in data if current_time <= x[0] < next_time]
        ip_pairs_in_chunk = set()
        for row in chunk_data:
            ip_pair = tuple(sorted([row[1], row[2]]))
            ip_pairs_in_chunk.add(ip_pair)
        
        for ip_pair in ip_pairs_in_chunk:
            chunk_counts[ip_pair] += 1
        
        current_time += timedelta(minutes=interval)
    
    sorted_counts = sorted(chunk_counts.items(), key=lambda x: -x[1])
    
    print(f"Top {output_rows} IP pairs by number of {interval}-minute chunks:")
    for i in range(min(output_rows, len(sorted_counts))):
        print(f"{i+1}. {sorted_counts[i][0]}: {sorted_counts[i][1]}")

if __name__ == '__main__':
    file_name_arg_index=1
    interval_arg_index=2
    output_rows_arg_index=3
    
    file_name=sys.argv[file_name_arg_index]
    
    if len(sys.argv)>interval_arg_index:
      interval=int(sys.argv[interval_arg_index])
      if len(sys.argv)>output_rows_arg_index:
          output_rows=int(sys.argv[output_rows_arg_index])
          process_csv(file_name,interval,output_rows)
      else:
          process_csv(file_name,interval)