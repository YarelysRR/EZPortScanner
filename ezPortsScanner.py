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

def port_scans(target, start_port=1, end_port=65535, max_threads=100, timeout=0.5):
    """Scan ports on the target IP within a specified range using multithreading."""
    print(f"Scanning target {target} from port {start_port} to {end_port}...\n")
    open_ports = []
    total_ports = end_port - start_port + 1
    scanned_ports = 0

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_port, target, port, timeout) for port in range(start_port, end_port + 1)]
        
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

def get_user_input():
    """Prompt the user to enter or adjust scan parameters."""
    target = input("Enter IP Address to scan: ")
    if not validate_ip(target):
        print("Invalid IP address format.")
        return get_user_input()
    
    start_port = int(input("Enter starting port (default 1): ") or 1)
    end_port = int(input("Enter ending port (default 1000): ") or 1000)
    max_threads = int(input("Enter maximum number of threads (default 100): ") or 100)
    timeout = float(input("Enter socket timeout in seconds (default 0.5): ") or 0.5)

    return target, start_port, end_port, max_threads, timeout

def main():
    """Main function for EZ Port Scanner program."""
    signal.signal(signal.SIGINT, signal_handler)
    
    target, start_port, end_port, max_threads, timeout = get_user_input()

    while True:
        # Confirm scan details with the user
        print(f"\nStarting scan on target {target}")
        print(f"Port range: {start_port} to {end_port}")
        print(f"Thread count: {max_threads}")
        print(f"Socket timeout: {timeout} seconds")
        
        confirm = input("Proceed with these settings? (Y/N or type 'exit' to quit): ").strip().lower()
        if confirm == 'y':
            # Start the port scan with the confirmed parameters
            port_scans(target, start_port, end_port, max_threads, timeout)
            break
        elif confirm == 'exit':
            print("Scan canceled. Exiting.")
            break
        else:
            print("Please enter new scan settings:")
            target, start_port, end_port, max_threads, timeout = get_user_input()

if __name__ == "__main__":
    main()
