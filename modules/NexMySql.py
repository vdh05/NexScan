#!/usr/bin/env python3
"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

import mysql.connector

def connectMySQL(host, user, password, userfile, passfile, verbose=False, stop_on_success=False):
    try:
        # Verbose logging
        if verbose:
            print(f"[DEBUG] Starting MySQL connection attempts on host: {host}")

        # Case 1: Direct username and password provided
        if user and password:
            try:
                if verbose:
                    print(f"[DEBUG] Trying to connect with user: {user} and password: {password}")
                mydb = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password
                )
                mydb.close()
                print(f'[\033[92m +\033[0m ] Successfully connected: {user} : {password}')
                if stop_on_success:
                    return True  # Stop on first success
            except mysql.connector.Error as e:
                if verbose:
                    print(f"[DEBUG] MySQL error for {user}:{password} - {e}")
                print(f'[\033[91m -\033[0m ] Failed to connect: {user} : {password}')

        # Case 2: Username provided, password file given
        elif user and passfile:
            if verbose:
                print(f"[DEBUG] Trying to connect with user: {user} and passwords from file: {passfile}")
            with open(passfile, 'r') as pf:
                passwords = [line.strip() for line in pf]

            for password in passwords:
                try:
                    if verbose:
                        print(f"[DEBUG] Trying password: {password}")
                    mydb = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=password
                    )
                    mydb.close()
                    print(f'[\033[92m +\033[0m ] Successfully connected: {user} : {password}')
                    if stop_on_success:
                        return True  # Stop on first success
                except mysql.connector.Error as e:
                    if verbose:
                        print(f"[DEBUG] MySQL error for {user}:{password} - {e}")
                    print(f'[\033[91m -\033[0m ] Failed to connect: {user} : {password}')

        # Case 3: Username file and password file given
        elif userfile and passfile:
            if verbose:
                print(f"[DEBUG] Trying users from file: {userfile} and passwords from file: {passfile}")
            with open(userfile, 'r') as uf:
                users = [line.strip() for line in uf]
            with open(passfile, 'r') as pf:
                passwords = [line.strip() for line in pf]

            for user in users:
                for password in passwords:
                    try:
                        if verbose:
                            print(f"[DEBUG] Trying user: {user} with password: {password}")
                        mydb = mysql.connector.connect(
                            host=host,
                            user=user,
                            password=password
                        )
                        mydb.close()
                        print(f'[\033[92m +\033[0m ] Successfully connected: {user} : {password}')
                        if stop_on_success:
                            return True  # Stop on first success
                    except mysql.connector.Error as e:
                        if verbose:
                            print(f"[DEBUG] MySQL error for {user}:{password} - {e}")
                        print(f'[\033[91m -\033[0m ] Failed to connect: {user} : {password}')

        # Case 4: Neither valid user nor password provided
        else:
            print('\033[91m[-]\033[0m Please provide a valid username and password or files containing credentials.')
            return False

        # If no successful login
        return False

    except KeyboardInterrupt:
        print('[\033[91m -\033[0m ] Detecting Keyboard Interrupt...Exiting...')
        exit(1)
