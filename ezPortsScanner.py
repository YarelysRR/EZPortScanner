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

def port_scans(target, start_port=1, end_port=1024, max_threads=100):
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
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("--start_port", type=int, default=1, help="Starting port (default 1)")
    parser.add_argument("--end_port", type=int, default=1024, help="Ending port (default 1024)")
    parser.add_argument("--threads", type=int, default=100, help="Maximum number of threads (default 100)")
    parser.add_argument("--timeout", type=float, default=0.5, help="Socket timeout in seconds (default 0.5)")
    return parser.parse_args()

def main():
    """Main function for EZ Port Scanner program."""
    args = parse_args()
    signal.signal(signal.SIGINT, signal_handler)
    
    # Validate IP address
    if not validate_ip(args.target):
        print("Invalid IP address format. Please enter a valid IP.")
        return
    
    # Confirm scan details with the user
    print(f"Starting scan on target {args.target}")
    print(f"Port range: {args.start_port} to {args.end_port}")
    print(f"Thread count: {args.threads}")
    print(f"Socket timeout: {args.timeout} seconds")
    
    confirm = input("Proceed with these settings? (Y/N): ").strip().lower()
    if confirm != 'y':
        print("Scan canceled.")
        return
    
    # Start the port scan
    port_scans(args.target, args.start_port, args.end_port, args.threads)

if __name__ == "__main__":
    main()
