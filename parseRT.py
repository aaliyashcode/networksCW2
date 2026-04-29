import re

#www.bijt.net
#traceroute to www.bijt.net (104.167.84.47), 30 hops ma
#www.ntua.gr
#traceroute to www.ntua.gr (147.102.224.101), 30 hops max, 60 byte packets
#



###
# with open('routetrace.log', 'r') as f:
#    log_file_lines = f.readlines()
#for line in log_file_lines:
 #   line = line.rstrip("\n")
  #  print(line)
#
 #   breakpoint()

from pathlib import Path

path = Path("routetrace.log")

with path.open("r", encoding="utf-8") as f:

    for line_number, line in enumerate(f, start=1):

        line = line.rstrip("\n")

print(f"{line_number}: {line}")



