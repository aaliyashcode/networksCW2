import re
import csv
import json

LOG_FILE = "routetrace.log"
OUTPUT_FILE = "routetrace.csv"

try:
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: {LOG_FILE} not found.")
    exit(1)

data = []
current_target = None
current_time = None
current_ip = None

SKIP_PREFIXES = ("traceroute")

for line in lines:
    line = line.strip()
    if not line:
        continue

    if line.startswith("# run_ts_utc="):
        current_time = line.split("=", 1)[1]

    elif line.startswith("#") and not line.startswith("# "):
        current_target = line[1:]

    elif not any(line.startswith(p) for p in SKIP_PREFIXES) and \
         "packet loss" not in line and \
         re.match(r'^[\w][\w\.\-]*\.[a-zA-Z]{2,}$', line):
        current_target = line

    elif "packet loss" in line:
        m = re.search(r'(\d+(?:\.\d+)?)%', line)
        current_loss = m.group(1) if m else None

    elif "rtt min/avg/max" in line:
        m = re.search(r'=\s*([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', line)
        if m and current_time and current_target and current_loss is not None:
            data.append([
                current_time,
                current_target,
                m.group(1),   # min
                m.group(2),   # avg
                m.group(3),   # max
                current_loss
            ])
            current_loss = None  # reset after appending

print(f"Parsed {len(data)} rows")
seen = set()
for row in data:
    if row[1] not in seen:
        print(f"  Target found: {row[1]} — sample: {row}")
        seen.add(row[1])

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Day","Time", "Target", "Hop No", "IP", "Time1", "Time2", "Time3"])
    writer.writerows(data)

print(f"Written to {OUTPUT_FILE}")


