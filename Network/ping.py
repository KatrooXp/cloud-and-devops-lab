# this script shows a route throught routers to destination host

import subprocess
import re

def trace_route(destination):
    max_hops = 30
    for ttl in range(1, max_hops + 1):
        ping_cmd = ["ping", "-c", "1", "-t", str(ttl), "-n", destination]
        result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        if "Time to live exceeded" in output or "time=" in output:
            # We've reached a router or the destination
            print(f"Hop {ttl}: {output}")
        else:
            # No response or unknown response
            print(f"Hop {ttl}: *")
            break

destination_host = input("Enter destination host: ")
trace_route(destination_host)

