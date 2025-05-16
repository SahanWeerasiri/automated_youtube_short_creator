# README

## Project Overview

`main.py` likely contains the main entry point and program logic.


## Project Structure

The project structure is as follows:

```
- main.py
```

## Project Details

This project contains the following files:

- main.py
### main.py
This Python script performs a port scan on a specified target IP address. Here's a breakdown:

**1. Setup and Initialization:**

- Imports necessary modules: `socket`, `threading`, `queue`, `os`, `re`, `subprocess`, `time`.
- Initializes a `Queue` called `portQueue` to hold port numbers to be scanned.
- Initializes an empty list `openPorts` to store discovered open ports.
- Initializes an empty list `threads` to store the threads created.

**2. Core Functions:**

- **`portScan(port)`:**
  - Attempts to establish a TCP connection to the `target` IP address on the given `port`.
  - Returns `True` if the connection succeeds (port is open), `False` otherwise.

- **`fillPorts(portList)`:**
  - Takes a list of `ports` as input.
  - Iterates through the `portList` and adds each port to the `portQueue`.

- **`worker()`:**
  - This is the function executed by each thread.
  - Continuously retrieves ports from the `portQueue` until the queue is empty.
  - Calls `portScan()` to check if the retrieved port is open.
  - If open, prints a message and appends the port to the `openPorts` list.
  - Calculates and prints a scan progress percentage and a progress bar to the console.  Crucially uses `end="\r"` to overwrite the progress output on each iteration.

- **`createThreads()`:**
  - Creates a specified number of threads (100 in this case).
  - Each thread is assigned the `worker()` function as its target.
  - Starts each thread and adds it to the `threads` list.

- **`getMyGateway()`:**
  - Uses `os.popen("ipconfig")` to execute the `ipconfig` command.
  - Parses the output to extract the IPv4 address of the default gateway using regular expressions.
  - Returns the gateway IP or `None` if not found.

- **`findAllIps()`:**
  - Gets the gateway IP using `getMyGateway()`.
  - Constructs the network prefix from the gateway IP.
  - Pings all possible IP addresses within the subnet (1 to 254) using `subprocess.Popen` with the `-n 1` (single ping) and `-w 100` (100ms timeout) options to populate the ARP table.  The output is redirected to `subprocess.DEVNULL` to avoid cluttering the console.
  - Waits for a short period (3 seconds) for the pings to complete.
  - Executes the `arp -a` command to retrieve the ARP table.
  - Parses the ARP table output to extract IP addresses using regular expressions.
  - Filters the IPs to only include those within the determined subnet.
  - Prints the list of found devices and returns it.

**3. Execution:**

- Calls `findAllIps()` to attempt to discover all active IP addresses on the local network.
- Prompts the user to enter the `target` IP address to scan.
- Fills the `portQueue` with port numbers from 1 to 1023.
- Creates and starts the thread pool using `createThreads()`.
- Waits for all threads to complete their work using `thread.join()`.
- Prints a "Scanning complete" message and displays the list of open ports found.

In summary, the script uses multithreading to efficiently scan a range of ports on a target IP address, identifying open TCP ports. It also includes functionality to discover IPs on the local network before prompting the user for a target.


