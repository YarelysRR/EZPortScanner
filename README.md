# EZ Port Scanning Tool

Welcome to **EZ Port Scanning**, a command-line (CLI) tool designed to make port scanning simple and efficient. This tool lets you scan for open ports on a target IP address, with options to customize the port range, set threading limits, and control socket timeouts. It’s a versatile tool, built with multithreading for faster scanning and flexibility in mind.

## Features

- **Multithreaded Scanning**: Allows you to scan large port ranges quickly by specifying the number of threads.
- **Configurable Port Range**: Scan all ports or a specific range based on your needs.
- **Socket Timeout Control**: Customize the timeout for each port scan attempt to adjust to various network environments.
- **Progress Indicator**: See scan progress in real-time, ideal for large port ranges.
- **Validation and Error Handling**: Input validation and interrupt handling ensure a smooth user experience.
- **Easy to Use**: CLI arguments let you customize your scan with minimal effort.

## Requirements

- **Python 3.x**: Ensure Python is installed on your system. You can download it from [Python’s official website](https://www.python.org/downloads/).
  
## Installation 

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ez-port-scanning.git
   cd ez-port-scanning


# USAGE

1. **Interactive Mode**
Run the tool with default parameters to scan ports 1 to 1000 on the target IP: ```python port_scanner.py <target IP>```

You will be prompted to enter the IP, port range, thread count, and timeout.

2. Command-Line Arguments

You can customize your scan directly, for example: ```python port_scanner.py <target_ip> --start_port <start> --end_port <end> --threads <threads> --timeout <timeout>```

# Example
To scan ports 1–1000 on 192.168.1.1 with 50 threads and a 1-second timeout: ```python port_scanner.py 192.168.1.1 --start_port 1 --end_port 1000 --threads 50 --timeout 1```

# Arguments
 | Argument	    |               Description	                        | Default |
 |--------------|---------------------------------------------------|---------|
 |<target_ip>   | The IP address to scan	                        | Required|
 |--start_port	| Starting port number	                            | 1       |
 |--end_port    | Ending port number	                            | 1000    |
 |--threads	    | Max concurrent threads	                        | 100     |
 |--timeout	    | Timeout (in seconds) for each port connection	    | 0.5     |

 


