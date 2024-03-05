import socket
import signal
import sys

def signal_handler(sig, frame):
    """Signal handler for Ctrl + C"""
    print("Thank you for using EZ Port Scanning!")
    sys.exit(0)

def port_scans(target):
    """Scan ports for a given target IP address and print open ports"""
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((target, port))

        if result == 0:
            print(f"Port {port} is open")

        sock.close()

def main():
    """Main function for the Easy Port Scanner program"""
    print("*** Welcome to Easy Port Scanning! ***")
    print("[Use Ctrl + C to quit at any time.]")

    # Set up a signal handler for Ctrl + C
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        target = input("Enter IP Address to scan (or type 'exit' to quit): ")

        if target.lower() in ['exit', 'quit']:
            print("Thank you for using EZ Port Scanning!")
            break

        print("*" * 30)
        print(f"*** Scanning: {target}  ***")
        print("*" * 30)

        port_scans(target)

        response = input("Would you like to scan another IP Address? Type Y / N: ")
        if response.upper() != 'Y':
            print("Thanks for using EZ Port Scanning!")
            break

if __name__ == "__main__":
    main()
