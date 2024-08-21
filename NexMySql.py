"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

import argparse
import mysql.connector

def connectMySQL(host, user, password, userfile=None, passfile=None):
    try:
        if userfile and passfile:
            with open (userfile, 'r') as userfile:
                users =  userfile.readlines()

            with open (passfile, 'r') as passfile:
                passwords = passfile.readlines()

            for user in users:
                user = user.strip()
                for password in passwords:
                    password = password.strip()
                    try:
                        mydb = mysql.connector.connect(
                            host=host,
                            user=user,
                            password=password
                        )
                        mydb.close()
                        print(f'\033[92m [+]\033[0m {user} : ', password)
                        break

                    except mysql.connector.Error as err:
                        print(f'\033[91m [-]\033[0m {user} : ', password)

        elif user and passfile:
            with open (passfile, 'r') as f:
                passwords = f.readlines()
            
            for password in passwords:
                try:
                    mydb = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=password
                    )
                    mydb.close()
                    print(f'[\033[92m + \033[0m] Successfully connected to MySQL database: {user}@{host}')

                except mysql.connector.Error as err:
                    print(f'\033[91m [-]\033[0m {user} : ', password)

        elif password and userfile:
            with open (userfile, 'r') as userfile:
                users = userfile.readlines()

            for user in users:
                try:
                    mydb = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=password
                    )
                    mydb.close()
                    print(f'[\033[92m + \033[0m] Successfully connected to MySQL database: {user}@{host}')

                except mysql.connector.Error as err:
                    print(f'\033[91m [-]\033[0m {user} : ', password)

    except KeyboardInterrupt:
        print('\033[[91m - \033[0m] Detecting Keyboard Interrupt...Exiting...')
        exit(1)
