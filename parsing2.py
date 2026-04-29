import re
import csv

INPUT_FILE = "routetrace copy.log"
OUTPUT_FILE = "routetrace-copy-csv.csv"

try:
    with open(INPUT_FILE, "r", errors="ignore") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: {INPUT_FILE} not found.")
    exit(1)

rows = []
current_time = None
current_target = None
destination_ip = None

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Timestamp: Wed 09 Apr 13:00:02 BST 2026
    if re.match(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{2}\s+\w+\s+\d{2}:\d{2}:\d{2}", line):
        current_time = line

    # Target: www.washington.edu
    elif re.match(r"^www\.", line):
        current_target = line
        destination_ip = None

    # Traceroute header: traceroute to www.washington.edu (128.208.60.208)
    elif line.startswith("traceroute to"):
        m = re.search(r"^traceroute to\s+(\S+)\s+\(([\d.]+)\)", line)
        if m:
            current_target = m.group(1)
            destination_ip = m.group(2)

    # Hop line: starts with a number
    elif re.match(r"^\d+\s+", line) and current_target:
        m = re.match(r"^(\d+)\s+(.*)", line)
        if not m:
            continue

        hop_number = m.group(1)
        hop_data = m.group(2)

        # Pure timeout: * * *
        # if hop_data.replace("*", "").replace(" ", "") == "":
        #     rows.append([
        #         current_time, current_target, destination_ip,
        #         hop_number, "*", "", "", "", ""
        #     ])
        #     continue

        # Extract all IPs and RTTs from the hop
        ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", hop_data)
        rtts = re.findall(r"(\d+\.\d+)\s+ms", hop_data)

        # First token tells us hostname vs IP
        first_token = hop_data.split()[0]
        ip_address = ips[0] if ips else first_token
        hostname = first_token if not re.match(r"^\d+\.\d+\.\d+\.\d+$", first_token) else ""

        rtt1 = rtts[0] if len(rtts) > 0 else ""
        rtt2 = rtts[1] if len(rtts) > 1 else ""
        rtt3 = rtts[2] if len(rtts) > 2 else ""

        rows.append([
            current_time, current_target, destination_ip,
            hop_number, ip_address,
            rtt1, rtt2, rtt3
        ])

print(f"Parsed {len(rows)} rows")
if rows:
    seen = set()
    for row in rows:
        if row[1] not in seen:
            print(f"  Target found: {row[1]} — sample: {row}")
            seen.add(row[1])

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "timestamp", "target", "destination_ip",
        "hop_number", "ip_address",
        "rtt1_ms", "rtt2_ms", "rtt3_ms"
    ])
    writer.writerows(rows)

print(f"Written to {OUTPUT_FILE}")