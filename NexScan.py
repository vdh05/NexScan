
#!/usr/bin/env python3
"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

import os
import argparse
import modules.NexSMB as NexSMB
import modules.NexFTP as NexFTP
import modules.NexSSH as NexSSH
import modules.NexMySql as NexMySql
import modules.NexDir as NexDir
import modules.NexSubD as NexSubD

# os.system('pip3 install -r requirements.txt')

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='This is a simple VAPT tool developed and managed by Nexeo Security (https://www.nexeosecurity.tech/).')

    # Add subparsers for each method
    subparsers = parser.add_subparsers(dest='method', help='Specify service')

    # FTP subparser
    ftp_parser = subparsers.add_parser('ftp', help='Specify service as FTP')
    ftp_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    ftp_parser.add_argument('-port', default=21, type=int, help='Port')
    ftp_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')  # Verbose flag
    ftp_parser.add_argument('-s', '--stop-on-success', action='store_true', help='Stop on first successful login')  # Stop on success flag

    group_ftp_user = ftp_parser.add_mutually_exclusive_group(required=True)
    group_ftp_user.add_argument('-u', '--user', type=str, help='Username')
    group_ftp_user.add_argument('-U', '--userfile', type=argparse.FileType('r'), default='./lists/user_list.txt', help='User file (default: ./lists/user_list.txt)')

    group_ftp_pass = ftp_parser.add_mutually_exclusive_group(required=True)
    group_ftp_pass.add_argument('-p', '--password', type=str, help='Password')
    group_ftp_pass.add_argument('-P', '--passwordfile', type=argparse.FileType('r'), default='./lists/password_list.txt', help='Password file (default: ./lists/password_list.txt)')

    # SSH subparser
    ssh_parser = subparsers.add_parser('ssh', help='Specify service as SSH')
    ssh_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    ssh_parser.add_argument('-port', default=22, type=int, help='Port')
    ssh_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    ssh_parser.add_argument('-s','--stop-on-success', action='store_true', help='Stop on first successful login')

    group_ssh_user = ssh_parser.add_mutually_exclusive_group(required=True)
    group_ssh_user.add_argument('-u', '--user', type=str, help='Username')
    group_ssh_user.add_argument('-U', '--userfile', type=argparse.FileType('r'), default='./lists/user_list.txt', help='User file (default: ./lists/user_list.txt)')

    group_ssh_pass = ssh_parser.add_mutually_exclusive_group(required=True)
    group_ssh_pass.add_argument('-p', '--password', type=str, help='Password')
    group_ssh_pass.add_argument('-P', '--passwordfile', type=argparse.FileType('r'), default='./lists/password_list.txt', help='Password file (default: ./lists/password_list.txt)')

    # SMB subparser
    smb_parser = subparsers.add_parser('smb', help='Specify service as SMB')
    smb_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    smb_parser.add_argument('-port', default=445, type=int, help='Port')
    smb_parser.add_argument('-s', '--share', type=str, help='Name of SMB Share (optional, will enumerate if not provided)')

    group_smb_user = smb_parser.add_mutually_exclusive_group(required=True)
    group_smb_user.add_argument('-u', '--user', type=str, help='Username')
    group_smb_user.add_argument('-U', '--userfile', type=argparse.FileType('r'), default='./lists/user_list.txt', help='User file (default: ./lists/user_list.txt)')
    
    group_smb_pass = smb_parser.add_mutually_exclusive_group(required=True)
    group_smb_pass.add_argument('-P', '--passwordfile', type=argparse.FileType('r'), default='./lists/password_list.txt', help='Password file (default: ./lists/password_list.txt)')
    group_smb_pass.add_argument('-p', '--password', type=str, help='Password')

    # MySQL subparser
    mysql_parser = subparsers.add_parser('mysql', help='Specify service as MySQL')
    mysql_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    mysql_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    mysql_parser.add_argument('-s', '--stop-on-success', action='store_true', help='Stop on first successful login')

    group_mysql_user = mysql_parser.add_mutually_exclusive_group(required=True)
    group_mysql_user.add_argument('-u', '--user', type=str, help='Username')
    group_mysql_user.add_argument('-U', '--userfile', type=argparse.FileType('r'), default='./lists/user_list.txt', help='User file (default: ./lists/user_list.txt)')

    group_mysql_pass = mysql_parser.add_mutually_exclusive_group(required=True)
    group_mysql_pass.add_argument('-p', '--password', type=str, help='Password')
    group_mysql_pass.add_argument('-P', '--passwordfile', type=argparse.FileType('r'), default='./lists/password_list.txt', help='Password file (default: ./lists/password_list.txt)')

    # Directory subparser
    directory_parser = subparsers.add_parser('directory', help='Perform Directory Fuzzing')
    directory_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    directory_parser.add_argument('-f', '--file', type=argparse.FileType('r'), default='./lists/directory_list.txt', help='Fuzzing File')
    directory_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    # Subdomain subparser
    subdomain_parser = subparsers.add_parser('subdomain', help='Perform Subdomain Fuzzing')
    subdomain_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    subdomain_parser.add_argument('-F', '--file', type=argparse.FileType('r'), default='./lists/subdomain_list.txt', help='Subdomain file')
    subdomain_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # Handle each method
    if args.method == 'ftp':
        userfile = None if not args.userfile else args.userfile.name
        passwordfile = None if not args.passwordfile else args.passwordfile.name
        NexFTP.bruteFTP(args.target, userfile, passwordfile, args.user, args.password, args.verbose, args.stop_on_success)
    
    elif args.method == 'ssh':
        userfile = None if not args.userfile else args.userfile.name
        passwordfile = None if not args.passwordfile else args.passwordfile.name
        NexSSH.ssh_bruteforce(args.target, args.port, userfile, passwordfile, args.user, args.password, args.verbose, args.stop_on_success)

    elif args.method == 'smb':
        userfile = None if not args.userfile else args.userfile.name
        passwordfile = None if not args.passwordfile else args.passwordfile.name
        NexSMB.fuzz_smb(args.user, args.password, args.target, args.share, args.port, userfile, passwordfile)

    elif args.method == 'mysql':
        userfile = None if not args.userfile else args.userfile.name
        passwordfile = None if not args.passwordfile else args.passwordfile.name
        NexMySql.connectMySQL(args.target, args.user, args.password, userfile, passwordfile, args.verbose, args.stop_on_success)

    elif args.method == 'directory':
        NexDir.fuzz(args.target, args.file.name, args.verbose) if args.file else NexDir.fuzz(args.target, verbose=args.verbose)

    elif args.method == 'subdomain':
        filtered_target = NexSubD.filter_url(args.target)
        NexSubD.fuzz(filtered_target, args.file.name, args.verbose) if args.file else NexSubD.fuzz(filtered_target, verbose=args.verbose)

if __name__ == '__main__':
    main()