# Persistent

This is a project based on a fairly old, but interesting perl script that breaks proxy log traffic up into five minute chunks, and then identifies clients that are communicating with the same destination repeatedly on a chunk by chunk basis. The idea was to take this perl script and see how well a chatbot could port it to Python, and how easily it could be modified to suit my own needs.  

The original script was created by Eric Conrad and is located here:
https://github.com/SMAPPER/NSM/blob/master/persistent.pl  

## Python Port

The script was ported from perl to python by Bing Chat AI as an expiriment. The entire contents of the file were submited to the AI (minus comments), and a few bug fixes were then submitted to the chatbot. The results are in `persistent.py`

A script to generate test logs that include simulated beaconing was also generated by the chatbot, and is included in `genlogs.py`.

## Generic Firewall version

The python script was then modified to take more generic input in the format of a CSV file in `fw-persistent.py`. The expected input format is:

```
timestamp,source_ip,dest_ip,bytes_sent,bytes_received
2023-03-03 18:50:28 UTC,10.0.329.52,65.124.136.145,737,808
2023-03-03 18:50:27 UTC,10.0.343.58,119.118.46.46,2973,714
```

Output using the perl version of the script and dummy log data created by `genlog.py`:

```
$ ./persistent.pl test.log | head
Count Client            Remote Site
------------------------------------------
 95   172.22.22.22      itsabeacon.com
  9   172.23.237.230    www.facebook.com
  9   172.23.79.42      www.facebook.com
  9   172.23.14.108     www.facebook.com
  9   172.23.168.61     www.facebook.com
  9   172.23.239.140    www.facebook.com
  9   172.23.140.228    www.amazon.com
  9   172.23.1.30       www.amazon.com
```

Using real data won't provide such clear results, but good enough for a POC.  

## Variations

Bing chat was prompted to re-create the original port of the persistent script, with the hope that it was coded in a more pythonic way. I think this was fairly successful. With some heavy filtering, this script has been useful. 

The 'new' version of the script is `3persistent.py`  

`4persistent.py` adds some analysis to the amount of data being transferred.  

`5persistent.py` adds a count of the total number of events for each IP pair, results from this script are useful if sorted by that count, like: `sort -rnk3 file.out`

`6persistent.py` adds a basic beacon rating that is probably not great - not yet tested

`7persistent.py` is an entirely new script written by bing chat, prompts are in the comments - not yet tested. 