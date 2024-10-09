#!/usr/bin/env python3
"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

import mysql.connector

def connectMySQL(host, user=None, password=None, userfile=None, passfile=None, verbose=False, stop_on_success=False):
    try:
        # Case 1: Direct username and password provided
        if user and password:
            if verbose:
                print(f"[*] Trying {user}:{password} on {host}")
            try:
                mydb = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password
                )
                mydb.close()
                print(f'\033[92m[+]\033[0m Successfully connected: {user} : {password}')
                if stop_on_success:
                    return True  # Stop on first success
            except mysql.connector.Error as err:
                if verbose:
                    print(f'\033[91m[-]\033[0m Failed to connect: {user} : {password}')
                    print(f"Error: {err}")

        # Case 2: Username from file, Password provided directly
        elif userfile and password:
            with open(userfile, 'r') as uf:
                users = [line.strip() for line in uf]
                
            for user in users:
                if verbose:
                    print(f"[*] Trying {user}:{password} on {host}")
                try:
                    mydb = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=password
                    )
                    mydb.close()
                    print(f'\033[92m[+]\033[0m Successfully connected: {user} : {password}')
                    if stop_on_success:
                        return True  # Stop on first success
                except mysql.connector.Error as err:
                    if verbose:
                        print(f'\033[91m[-]\033[0m Failed to connect: {user} : {password}')
                        print(f"Error: {err}")

        # Case 3: Username and password files provided
        elif userfile and passfile:
            with open(userfile, 'r') as uf:
                users = [line.strip() for line in uf]
            with open(passfile, 'r') as pf:
                passwords = [line.strip() for line in pf]

            for user in users:
                for password in passwords:
                    if verbose:
                        print(f"[*] Trying {user}:{password} on {host}")
                    try:
                        mydb = mysql.connector.connect(
                            host=host,
                            user=user,
                            password=password
                        )
                        mydb.close()
                        print(f'\033[92m[+]\033[0m Successfully connected: {user} : {password}')
                        if stop_on_success:
                            return True  # Stop on first success
                    except mysql.connector.Error as err:
                        if verbose:
                            print(f'\033[91m[-]\033[0m Failed to connect: {user} : {password}')
                            print(f"Error: {err}")

        return False  # No successful login

    except KeyboardInterrupt:
        print('\033[91m[-]\033[0m Detecting Keyboard Interrupt...Exiting...')
        exit(1)
