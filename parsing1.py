import re
import csv

LOG_FILE = "routetrace copy.log"
OUTPUT_FILE = "routetrace1.csv"

try:
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: {LOG_FILE} not found.")
    exit(1)

data = []
# State variables to keep track of which trace we are in
current_day = None
current_time = None
current_website = None

# Regex Patterns
# 1. Matches: 09 Apr 13:00:02
date_re = re.compile(r"(?P<day>\d{2})\s+(?P<month>\w{3})\s+(?P<time>\d{2}:\d{2}:\d{2})")
# 2. Matches website names (lines starting with www.)
site_re = re.compile(r"^(www\.[a-z0-9.-]+)$")
# 3. Matches Hops: number, IP, and 3 delay values
hop_re = re.compile(r"^\s*(?P<hop>\d+)\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+(?P<t1>[\d.]+)\s+ms.*?\s+(?P<t2>[\d.]+)\s+ms.*?\s+(?P<t3>[\d.]+)\s+ms")

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Step 1: Extract Date and Time
    # (Matches lines like: Wed 09 Apr 13:00:02 BST 2026)
    date_match = date_re.search(line)
    if date_match:
        current_day = f"{date_match.group('day')} {date_match.group('month')}"
        current_time = date_match.group('time')
        continue

    # Step 2: Extract Website
    # (Matches lines like: www.washington.edu)
    site_match = site_re.search(line)
    if site_match:
        current_website = site_match.group(1)
        continue

    # Step 3: Extract Hop Data
    # If it's a hop line, we append a full row to our data list
    hop_match = hop_re.search(line)
    if hop_match:
        h = hop_match.groupdict()
        if current_website and current_day:
            data.append([
                current_day,      # Day/Month
                current_time,     # Timestamp
                current_website,  # Target Website
                h['hop'],         # Hop Number
                h['ip'],          # IP Address
                h['t1'],          # Delay 1
                h['t2'],          # Delay 2
                h['t3']           # Delay 3
            ])

print(f"Parsed {len(data)} hop rows.")

# Write to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Day", "Time", "Website", "Hop No", "IP", "Time1", "Time2", "Time3"])
    writer.writerows(data)

print(f"Successfully written to {OUTPUT_FILE}")