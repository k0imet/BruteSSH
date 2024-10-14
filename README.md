# BruteSSH
A simple tool in python for SSH bruteforce

### Usage

```bash
┌──(root㉿kali)-[~]
└─# python3 brutessh.py                                                  
 ____             _       ____ ____  _   _ 
| __ ) _ __ _   _| |_ ___/ ___/ ___|| | | |                                  
|  _ \| '__| | | | __/ _ \___ \___ \| |_| |                                  
| |_) | |  | |_| | ||  __/___) |__) |  _  |                                  
|____/|_|   \__,_|\__\___|____/____/|_| |_|                                  
                                                                             
                                                                             
usage: brutessh.py [-h] -t TARGET_HOST [-p PORT] [-U USERNAME_LIST]
                   [-u USERNAME] -P PASSWORD_LIST [-T THREADS]
                   [--mode {wordlist,spray}]
brutessh.py: error: the following arguments are required: -t/--target-host, -P/--password-list
```

## Key Features Added:
Single Username Support: You can now specify a single username via the -u or --username argument. If a single username is provided, the script will use that instead of a username list.

Example:

```bash
python3 brutessh.py -t <target-host> -p 22 -u admin -P password_list.txt
```
Password Spraying Mode: You can use the --mode spray argument to enable password spraying, where a single password (or password list) is tried across multiple usernames.

Example for password spraying:

```bash
python3 brutessh.py -t <target-host> -p 22 -U username_list.txt -P password_list.txt --mode spray
``` 
In this mode, the script tries each password across all usernames before moving to the next password, as is typical in password spraying attacks.

Backward Compatibility: The tool is still compatible with the original wordlist mode where multiple usernames and passwords are tried in combination.

### Usage Examples:

- Traditional Wordlist Attack (multiple usernames and passwords):

```bash
python3 brutessh.py -t <target-host> -p 22 -U username_list.txt -P password_list.txt
```

- Single Username, Multiple Passwords:

```bash
python3 brutessh.py -t <target-host> -p 22 -u admin -P password_list.txt
```

- Password Spraying (same password across multiple usernames):

```bash
python3 brutessh.py -t <target-host> -p 22 -U username_list.txt -P password_list.txt --mode spray
```

This updated version provides more flexibility for different types of brute-force and spraying attacks, while still maintaining the original wordlist functionality.
