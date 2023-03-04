# Created by AI with the following prompt:
# Generate 8 hours of realistic proxy logs consisting of traffic from a private network to popular websites consisting of 1000 requests per minute. 
# There should also be beacon traffic between the client IP "172.22.22.22" and the domain "http://itsabeacon.com/asdfasdfasdf"

import random
from datetime import datetime, timedelta

def generate_proxy_logs():
    start_time = datetime(2022, 1, 1)
    end_time = start_time + timedelta(hours=8)
    current_time = start_time
    beacon_ip = "172.22.22.22"
    beacon_url = "http://itsabeacon.com/asdfasdfasdf"
    
    popular_urls = ["http://www.google.com", "http://www.facebook.com", "http://www.youtube.com", "http://www.amazon.com"]
    
    while current_time < end_time:
        for i in range(1000):
            source_ip = f"172.23.{random.randint(0,255)}.{random.randint(0,255)}"
            destination_url = random.choice(popular_urls)
            log_line = f'{source_ip} - - [{current_time.strftime("%d/%b/%Y:%H:%M:%S %z")}] "GET {destination_url} HTTP/1.0" 200 {random.randint(1000,5000)} TCP_MISS:DIRECT'
            print(log_line)
        
        beacon_log_line = f'{beacon_ip} - - [{current_time.strftime("%d/%b/%Y:%H:%M:%S %z")}] "GET {beacon_url} HTTP/1.0" 200 {random.randint(1000,5000)} TCP_MISS:DIRECT'
        print(beacon_log_line)
        
        current_time += timedelta(minutes=1)

generate_proxy_logs()