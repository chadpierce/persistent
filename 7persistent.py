'''
> can you do a better analysis to generate the beacon rating?

The beacon rating in the modified script is calculated as the ratio of the number of unique time chunks to the total number of connections between the IP pair. This is a simple way to calculate a beacon rating and can be used as a starting point for further analysis.
There are other ways to calculate a beacon rating that may provide more accurate results. For example, you could use statistical methods to analyze the distribution of connection times between IP pairs and identify regular patterns. However, this would require more advanced analysis and is beyond the scope of this script.
Is there anything else you would like me to do?

> can you write a new script that uses statistical methods to analyze the distribution of connection times between IP pairs and identify regular patterns?

Sure! Here is a script that uses statistical methods to analyze the distribution of connection times between IP pairs and identify regular patterns. This script calculates the mean and standard deviation of the time intervals between connections for each IP pair. It then calculates a z-score for each time interval, which measures how many standard deviations away from the mean it is. A high z-score indicates that the time interval is regular and may be part of a beacon.

'''

import csv
from collections import defaultdict
from datetime import datetime
import sys
import numpy as np

input_file = sys.argv[1]
output_rows = 10

timestamp_col = 0
source_ip_col = 1
dest_ip_col = 2

def get_seconds(timestamp):
    dt = datetime.strptime(timestamp, '%Y-%m-%d-%H:%M:%S')
    return (dt - datetime(1970,1,1)).total_seconds()

with open(input_file) as f:
    reader = csv.reader(f)
    #next(reader) # skip header row
    timestamps = defaultdict(list)
    for row in reader:
        timestamp, source_ip, dest_ip = row[timestamp_col], row[source_ip_col], row[dest_ip_col]
        seconds = get_seconds(timestamp)
        timestamps[(source_ip, dest_ip)].append(seconds)

beacon_ratings = {}
for pair in timestamps:
    intervals = np.diff(sorted(timestamps[pair]))
    mean_interval = np.mean(intervals)
    std_interval = np.std(intervals)
    if std_interval == 0:
        beacon_ratings[pair] = float('inf')
    else:
        z_scores = (intervals - mean_interval) / std_interval
        beacon_rating = np.mean(np.abs(z_scores))
        beacon_ratings[pair] = beacon_rating

sorted_beacon_ratings = sorted(beacon_ratings.items(), key=lambda x: x[1])

for pair, beacon_rating in sorted_beacon_ratings[:output_rows]:
    print(f'{pair[0]},{pair[1]} - {beacon_rating:.2f}')