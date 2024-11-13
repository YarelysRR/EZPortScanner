# EZ Port Scanning Tool

EZ Port Scanner is a flexible and efficient port scanner for scanning open ports on a target IP. It supports both command-line arguments for advanced users and an interactive mode for ease of use.

## Features
- **Scan All Ports**: Scans from port 1 to 65535 (default is ports 1-1000).
- **Multithreaded**: Optimized for speed using multiple threads.
- **Customizable Settings**: Users can set specific port ranges, timeout, and thread count.
- **Interactive Mode**: If arguments aren’t provided, the tool will prompt for settings interactively.

## Requirements
- Python 3.x

## Installation
Clone this repository:
```bash
git clone https://github.com/yourusername/ezPortScanner.git
cd ezPortScanner


# USAGE
You can run EZ Port Scanning Tool in two ways:

1. Command Line Mode

```python3 ezPortScanner.py <target IP>``` or ```python3 ezPortScanner.py <target_ip> [--start_port <start>] [--end_port <end>] [--threads <count>] [--timeout <seconds>]```

2. **Interactive Mode**
Run without arguments, and the tool will prompt for necessary details:
```python3 ezPortScanner.py```


# Arguments

 | Argument	    |               Description	                        | Default |
 |--------------|---------------------------------------------------|---------|
 |<target_ip>   | The IPV4 address to scan	                         | N/A     |
 |--start_port	 | Starting port number	                             | 1       |
 |--end_port    | Ending port number	                               | 1000    |
 |--threads	    | Max concurrent threads	                           | 100     |
 |--timeout	    | Timeout (in seconds) for each port connection	    | 0.5     |




