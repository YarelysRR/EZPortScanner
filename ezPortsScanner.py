import socket
import signal
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def signal_handler(sig, frame):
    """Signal handler for Ctrl + C."""
    print("\nThank you for using EZ Port Scanning!")
    sys.exit(0)

def validate_ip(ip):
    """Validate that the provided IP address has a valid format."""
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(pattern, ip):
        return all(0 <= int(num) <= 255 for num in ip.split('.'))
    return False

def scan_port(target, port, timeout=0.5):
    """Check if a specific port is open on the target IP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((target, port))
        if result == 0:
            return port
    finally:
        sock.close()
    return None

def port_scans(target, start_port=1, end_port=65535, max_threads=100):
    """Scan ports on the target IP within a specified range using multithreading."""
    print(f"Scanning target {target} from port {start_port} to {end_port}...\n")
    open_ports = []
    total_ports = end_port - start_port + 1
    scanned_ports = 0
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(start_port, end_port + 1)]
        
        for future in as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
                print(f"Port {port} is open")
            
            # Show progress
            scanned_ports += 1
            progress = (scanned_ports / total_ports) * 100
            print(f"Progress: {progress:.2f}%", end="\r")
    
    print("\nScan complete.")
    if open_ports:
        print("Open ports:", ", ".join(str(port) for port in open_ports))
    else:
        print("No open ports found.")

def parse_args():
    """Parse command-line arguments for the port scanner."""
    parser = argparse.ArgumentParser(description="EZ Port Scanning Tool")
    parser.add_argument("target", nargs="?", help="Target IP address")
    parser.add_argument("--start_port", type=int, default=None, help="Starting port (default 1)")
    parser.add_argument("--end_port", type=int, default=None, help="Ending port (default 1000)")
    parser.add_argument("--threads", type=int, default=None, help="Maximum number of threads (default 100)")
    parser.add_argument("--timeout", type=float, default=None, help="Socket timeout in seconds (default 0.5)")
    return parser.parse_args()

def main():
    """Main function for EZ Port Scanner program."""
    args = parse_args()
    signal.signal(signal.SIGINT, signal_handler)
    
    # Gather target and settings, prompting user if any are missing
    target = args.target or input("Enter IP Address to scan: ")
    if not validate_ip(target):
        print("Invalid IP address format. Please enter a valid IP.")
        return
    
    start_port = args.start_port if args.start_port is not None else int(input("Enter starting port (default 1): ") or 1)
    end_port = args.end_port if args.end_port is not None else int(input("Enter ending port (default 1000): ") or 1000)
    max_threads = args.threads if args.threads is not None else int(input("Enter maximum number of threads (default 100): ") or 100)
    timeout = args.timeout if args.timeout is not None else float(input("Enter socket timeout in seconds (default 0.5): ") or 0.5)
    
    # Confirm or modify scan details with the user
    while True:
        print(f"Starting scan on target {target}")
        print(f"Port range: {start_port} to {end_port}")
        print(f"Thread count: {max_threads}")
        print(f"Socket timeout: {timeout} seconds")
        
        confirm = input("Proceed with these settings? (Y to continue, N to modify, exit to quit): ").strip().lower()
        if confirm == 'y':
            break
        elif confirm == 'exit':
            print("Scan canceled.")
            return
        else:
            # Allow user to re-enter settings interactively if needed
            target = input("Enter IP Address to scan: ") if not args.target else target
            start_port = int(input(f"Enter starting port (default {start_port}): ") or start_port)
            end_port = int(input(f"Enter ending port (default {end_port}): ") or end_port)
            max_threads = int(input(f"Enter maximum number of threads (default {max_threads}): ") or max_threads)
            timeout = float(input(f"Enter socket timeout in seconds (default {timeout}): ") or timeout)
    
    # Start the port scan
    port_scans(target, start_port, end_port, max_threads)

if __name__ == "__main__":
    main()
