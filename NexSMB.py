"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

import argparse
from smb.SMBConnection import SMBConnection

def fuzz_smb(user, password, target,share, port,userfile=None, passfile=None):
    my_name = "user"
    remote_name = "remote user"

    print('\nFuzzing SMB with user: {}, password: {}, target: {}, port: {}\n'.format(user, password, target, port))
    
    if passfile and user:
        with open(passfile, 'r') as f:
            passwords = f.readlines()
        for password in passwords:
            password = password.strip()
            conn = SMBConnection(user, password,my_name,remote_name, use_ntlm_v2=True)
            flag = conn.connect(target, 139)
            if flag:
                print(f'\033[92m [+]\033[0m {user} : ', password)
                break
            else:
                print(f'\033[91m [-]\033[0m {user} : ', password)

    elif userfile and password:
        with open(userfile, 'r') as f:
            users = f.readlines()
        for user in users:
            user = user.strip()
            conn = SMBConnection(user, password,my_name,remote_name, use_ntlm_v2=True)
            flag = conn.connect(target, 139)
            if flag:
                print(f'\033[92m [+]\033[0m {user} : ', password)
                break
            else:
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

                conn = SMBConnection(user, password,my_name,remote_name, use_ntlm_v2=True)
                flag = conn.connect(target, 139)
                if flag:
                    print(f'\033[92m [+]\033[0m {user} : ', password)
                    break
                else:
                    print(f'\033[91m [-]\033[0m {user} : ', password)


    else:
        print('\033[91m [-]\033[0m Please provide both username and password files')
        exit(1)
        