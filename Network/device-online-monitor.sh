#!/bin/bash

# this script monitors changes in the ARP table of the router in local network (task 5c)

# Function to run arp-scan and capture its output
get_arp_scan() {
    sudo arp-scan --localnet | grep -E '^([0-9]{1,3}\.){3}[0-9]{1,3}'
}

# Declare an associative array to store the previous ARP scan results
previous_arp_scan=$(get_arp_scan)

while true; do
    # Capture the current ARP scan
    current_arp_scan=$(get_arp_scan)

    # Compare the current scan with the previous scan
    diff_output=$(diff <(echo "$current_arp_scan") <(echo "${previous_arp_scan["ARP"]:-}"))


    # Check if there are any differences
    if [ -n "$diff_output" ]; then
        while read -r line; do
            if [[ "$line" =~ ^\> ]]; then
                echo "Device is lost: ${line:2}"
            elif [[ "$line" =~ ^\< ]]; then
                echo "New device detected: ${line:2}"
            fi
        done <<< "$diff_output"
    fi

    # Update the previous ARP scan with the current scan for the next iteration
    previous_arp_scan=$current_arp_scan

    # Wait for 5 seconds before the next scan
    sleep 5
done

