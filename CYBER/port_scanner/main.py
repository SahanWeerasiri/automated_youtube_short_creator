import socket
import threading 
from queue import Queue
import os
import re
import subprocess
import time

portQueue = Queue() # Create a queue for the ports
openPorts = [] # List to store open ports
threads = [] # List to store threads

def portScan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Intenet socket, # TCP socket
        sock.connect((target, port)) # Connect to the target and port
        return True # If the connection is successful, the port is open
    except:
        return False # If the connection fails, the port is closed

def fillPorts(portList):
    for ports in portList:
        portQueue.put(ports)

def worker():
    while not portQueue.empty(): # While the queue is not empty
        port = portQueue.get() # Get a port from the queue
        if portScan(port): # If the port is open
            print(f"Port {port} is open") # Print the open port
            openPorts.append(port) # Add the open port to the list
        progress = ((1024 - portQueue.qsize()) / 1024) * 100
        print(f"Scanning Progress... {progress:.2f}%") # Print the number of ports left
        #Print a progress bar
        print("[" + "#" * int(progress) + " " * (100 - int(progress)) + "]", end="\r")

def createThreads():
    for _ in range(100): # Create 10 threads
        thread = threading.Thread(target=worker) # Create a thread
        thread.start() # Start the thread
        threads.append(thread) # Add the thread to the list

def getMyGateway():
    ip = os.popen("ipconfig").read() # Get the IP configuration
    ip = re.findall(r"IPv4 Address.*?: (\d+\.\d+\.\d+\.\d+)", ip) # Find the IPv4 address
    return ip[0] if ip else None # Return the IPv4 address

def findAllIps():
    gateway_ip = getMyGateway()
    if not gateway_ip:
        print("No gateway IP found.")
        return []

    # Get the network prefix (e.g., 192.168.1.)
    ip_parts = gateway_ip.split(".")
    network_prefix = ".".join(ip_parts[:3]) + "."

    # Ping the whole subnet to populate ARP table
    print("Pinging subnet to populate ARP table...")
    for i in range(1, 255):
        ip = f"{network_prefix}{i}"
        subprocess.Popen(["ping", "-n", "1", "-w", "100", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait a bit for pings to finish
    time.sleep(3)

    # Get ARP table
    arp_output = os.popen("arp -a").read()
    ips = re.findall(r"(\d+\.\d+\.\d+\.\d+)", arp_output)
    # Filter only IPs in our subnet
    subnet_ips = [ip for ip in ips if ip.startswith(network_prefix)]
    print(f"Devices found: {subnet_ips}")
    return subnet_ips
    
findAllIps() # Find all IPs in the subnet
target = input("Enter the target IP address: ") # Get the target IP address from the user
if not target:
    print("No target IP provided.")
    exit(1)
print("Filling the queue with ports...") # Print that the queue is being filled

fillPorts(range(1, 1024)) # Fill the queue with ports from 1 to 1024
createThreads() # Create the threads
for thread in threads: # Wait for all threads to finish
    thread.join() # Wait for the thread to finish

print("Scanning complete.") # Print that the scanning is complete
print(f"Open ports: {openPorts}") # Print the list of open ports