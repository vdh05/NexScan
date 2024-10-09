#!/usr/bin/env python3
"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

from smb.SMBConnection import SMBConnection

# Function to list available shares (for public and authenticated sessions)
def list_smb_shares(target, user=None, password=None, port=445):
    my_name = "NexScan"
    remote_name = "Target"

    try:
        # Create SMBConnection with or without credentials
        conn = SMBConnection(user or '', password or '', my_name, remote_name, use_ntlm_v2=True)
        if conn.connect(target, port):
            shares = conn.listShares()
            print("\n\033[94m[*]\033[0m Available SMB Shares:")
            for share in shares:
                print(f"  \033[92m[+]\033[0m {share.name} - {share.comments}")
            return [share.name for share in shares]
        else:
            print(f"\033[91m[-]\033[0m Could not connect to {target} using {user or 'guest'}")
            return []
    except Exception as e:
        print(f"\033[91m[-]\033[0m Error listing shares: {e}")
        return []

# Function to enumerate public SMB shares (guest access)
def enum_public_shares(target, port=445):
    print(f"\n\033[94m[*]\033[0m Enumerating public SMB shares on {target}...\n")
    return list_smb_shares(target, port=port)

# Function to brute-force SMB credentials and list shares after authentication
def fuzz_smb(user, password, target, share=None, port=445, userfile=None, passfile=None):
    my_name = "NexScan"
    remote_name = "Target"

    # Enumerate public shares (guest access)
    public_shares = enum_public_shares(target, port)

    # Brute-force with provided credentials or files
    print(f'\nFuzzing SMB with user: {user}, password: {password}, target: {target}, port: {port}\n')

    # Case 1: Direct user and password provided
    if user and password:
        conn = SMBConnection(user, password, my_name, remote_name, use_ntlm_v2=True)
        if conn.connect(target, port):
            print(f'\033[92m[+]\033[0m Successfully connected: {user}:{password}')
            print("\n\033[94m[*]\033[0m Enumerating SMB shares after successful login...\n")
            authenticated_shares = list_smb_shares(target, user, password, port)
        else:
            print(f'\033[91m[-]\033[0m Failed to connect: {user}:{password}')

    # Case 2: Username from file and password from input
    elif userfile and password:
        with open(userfile, 'r') as f:
            users = [line.strip() for line in f]
        for user in users:
            conn = SMBConnection(user, password, my_name, remote_name, use_ntlm_v2=True)
            if conn.connect(target, port):
                print(f'\033[92m[+]\033[0m Successfully connected: {user}:{password}')
                print("\n\033[94m[*]\033[0m Enumerating SMB shares after successful login...\n")
                authenticated_shares = list_smb_shares(target, user, password, port)
                break
            else:
                print(f'\033[91m[-]\033[0m Failed to connect: {user}:{password}')
    
    # Case 3: Username from input and password from file
    elif passfile and user:
        with open(passfile, 'r') as f:
            passwords = [line.strip() for line in f]
        for password in passwords:
            conn = SMBConnection(user, password, my_name, remote_name, use_ntlm_v2=True)
            if conn.connect(target, port):
                print(f'\033[92m[+]\033[0m Successfully connected: {user}:{password}')
                print("\n\033[94m[*]\033[0m Enumerating SMB shares after successful login...\n")
                authenticated_shares = list_smb_shares(target, user, password, port)
                break
            else:
                print(f'\033[91m[-]\033[0m Failed to connect: {user}:{password}')
    
    # Case 4: Both username and password files provided
    elif userfile and passfile:
        with open(userfile, 'r') as f:
            users = [line.strip() for line in f]
        with open(passfile, 'r') as f:
            passwords = [line.strip() for line in f]
        for user in users:
            for password in passwords:
                conn = SMBConnection(user, password, my_name, remote_name, use_ntlm_v2=True)
                if conn.connect(target, port):
                    print(f'\033[92m[+]\033[0m Successfully connected: {user}:{password}')
                    print("\n\033[94m[*]\033[0m Enumerating SMB shares after successful login...\n")
                    authenticated_shares = list_smb_shares(target, user, password, port)
                    break
                else:
                    print(f'\033[91m[-]\033[0m Failed to connect: {user}:{password}')
    
    else:
        print('\033[91m[-]\033[0m Please provide both username and password files or direct input')
        exit(1)
