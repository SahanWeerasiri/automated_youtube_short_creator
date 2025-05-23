import os
import sys
import time
from collections import defaultdict
from scapy.all import sniff, IP # analyze network packets

THRESHOLD = 5  # Threshold for DoS detection
print("THRESHOLD: ", THRESHOLD)

def packet_callback(packet):
    src_ip = packet[IP].src
    packet_count[src_ip] += 1
    current_time = time.time()
    time_interval = current_time - start_time[0]

    if time_interval > 1:
        for ip, count in packet_count.items():
            packet_rate = count / time_interval

            if packet_rate > THRESHOLD and ip not in blocked_ips:
                print(f"Blocking IP: {ip} - Packet Rate: {packet_rate:.2f} packets/sec")
                os.system(f"iptables -A INPUT -s {ip} -j DROP")
                blocked_ips.add(ip)
        # Reset the packet count and start time for the next interval
        packet_count.clear()
        start_time[0] = current_time

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)
    
    packet_count = defaultdict(int)  # Dictionary to count packets from each IP
    blocked_ips = set()  # Set to keep track of blocked IPs
    start_time = [time.time()]  # List to keep track of the start time

    print("Starting packet sniffing...")
    # Start sniffing packets
    sniff(prn=packet_callback, filter="ip")