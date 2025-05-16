# README

## Project Overview

Okay, based on the file name provided:

*   **main.py**: This suggests this file is likely the primary entry point or starting point of a Python program. It likely contains the main execution logic and potentially imports and utilizes code from other modules.


## Project Structure

The project structure is as follows:

```
- main.py
```

## Project Details

This project contains the following files:

- main.py
### main.py
This Python code performs a port scan on a specified target IP address to identify open ports. Here's a breakdown:

1.  **Initialization:**
    *   Imports necessary libraries like `socket`, `threading`, `queue`, `os`, `re`, `subprocess`, and `time`.
    *   Creates a `portQueue` (Queue) to hold port numbers to be scanned.
    *   Creates an `openPorts` (list) to store discovered open ports.
    *   Creates a `threads` (list) to store the thread objects.

2.  **`portScan(port)` Function:**
    *   Attempts to establish a TCP connection to the specified `target` IP address on the given `port`.
    *   Returns `True` if the connection is successful (port is open), `False` otherwise.

3.  **`fillPorts(portList)` Function:**
    *   Takes a list of ports and populates the `portQueue` with them.

4.  **`worker()` Function:**
    *   This function is executed by each thread.
    *   Continuously retrieves ports from the `portQueue` until it's empty.
    *   Calls `portScan()` to check if the retrieved port is open.
    *   If the port is open, prints a message and adds it to the `openPorts` list.
    *   Prints a scan progress percentage and a simple progress bar.

5.  **`createThreads()` Function:**
    *   Creates a specified number of threads (currently 100).
    *   Each thread is assigned the `worker()` function to execute.
    *   Starts each thread and adds it to the `threads` list.

6.  **`getMyGateway()` Function:**
    *   Uses the `ipconfig` command (Windows) to get the system's IP configuration.
    *   Extracts the IPv4 address of the gateway using regular expressions.
    *   Returns the gateway IP address, or `None` if not found.

7.  **`findAllIps()` Function:**
    *   Gets the gateway IP using `getMyGateway()`.
    *   Constructs the network prefix (e.g., 192.168.1.) based on the gateway IP.
    *   Pings all possible IP addresses in the subnet to populate the ARP table which maps IP addresses to MAC addresses. This makes it possible to scan all reachable IPs.  Uses `subprocess.Popen` to run the `ping` command in the background without displaying output.
    *   Waits for the pings to complete using `time.sleep()`.
    *   Retrieves the ARP table using the `arp -a` command.
    *   Extracts all IP addresses from the ARP table using regular expressions.
    *   Filters the IPs to only include those within the local subnet.
    *   Prints the list of discovered devices.

8.  **Main Execution Block:**
    *   Calls `findAllIps()` to discover IPs on the network.
    *   Prompts the user to enter the `target` IP address to scan.
    *   Validates that a target IP was provided.
    *   Prints a message indicating that the queue is being filled.
    *   Calls `fillPorts()` to add ports 1-1023 to the `portQueue`.
    *   Calls `createThreads()` to create and start the scanning threads.
    *   Waits for all threads to finish using `thread.join()`.
    *   Prints a completion message and displays the list of open ports.

In essence, the code is a multithreaded port scanner that first attempts to discover hosts on the local network and then scans the user-provided target IP address to find open TCP ports. It uses threading to speed up the scanning process by scanning multiple ports concurrently.


