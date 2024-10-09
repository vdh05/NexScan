#!/usr/bin/env python3
"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

import os
import argparse
import NexSMB
import NexFTP
import NexSSH
import NexMySql
import NexDir
import NexSubD

# os.system('pip3 install -r requirements.txt')

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='This is a simple VAPT tool developed and managed by Nexeo Security (https://www.nexeosecurity.tech/).')

    # Add subparsers for each method
    subparsers = parser.add_subparsers(dest='method', help='Specify service')

    # FTP subparser
    ftp_parser = subparsers.add_parser('ftp', help='Specify service as FTP')
    ftp_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    ftp_parser.add_argument('-u', '--user', required=False, type=str, help='Username')
    ftp_parser.add_argument('-U', '--userfile', type=argparse.FileType('r'), help='User file')
    ftp_parser.add_argument('-P', '--passwordfile', type=argparse.FileType('r'), help='Password file')
    ftp_parser.add_argument('-p', '--password', type=str, help='Password')
    ftp_parser.add_argument('-port', default=21, type=int, help='Port')

    # SSH subparser
    ssh_parser = subparsers.add_parser('ssh', help='Specify service as SSH')
    ssh_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    ssh_parser.add_argument('-u', '--user', type=str, required=False, help='Username')
    ssh_parser.add_argument('-U', '--userfile', type=argparse.FileType('r'), default='./unix_users.txt', help='User file (default: ./unix_users.txt)')
    ssh_parser.add_argument('-P', '--passwordfile', type=argparse.FileType('r'), default='./unix_passwords.txt', help='Password file (default: ./unix_passwords.txt)')
    ssh_parser.add_argument('-p', '--password', type=str, required=False, help='Password')
    ssh_parser.add_argument('-port', default=22, type=int, help='Port')
    ssh_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    ssh_parser.add_argument('-s','--stop-on-success', action='store_true', help='Stop on first successful login')

    # SMB subparser
    smb_parser = subparsers.add_parser('smb', help='Specify service as SMB')
    smb_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    smb_parser.add_argument('-port', default=445, type=int, help='Port')
    smb_parser.add_argument('-s', '--share', type=str, help='Name of SMB Share')

    group_smb_pass = smb_parser.add_mutually_exclusive_group(required=True)
    group_smb_pass.add_argument('-P', '--passwordfile', type=argparse.FileType('r'), help='Password file')
    group_smb_pass.add_argument('-p', '--password', type=str, help='Password')

    group_smb_user = smb_parser.add_mutually_exclusive_group(required=True)
    group_smb_user.add_argument('-u', '--user', type=str, help='Username')
    group_smb_user.add_argument('-U', '--userfile', type=argparse.FileType('r'), help='User file')

    # MySQL subparser
    mysql_parser = subparsers.add_parser('mysql', help='Specify service as MySQL')
    mysql_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    mysql_parser.add_argument('-u', '--user', type=str, help='Username')
    mysql_parser.add_argument('-p', '--password', type=str, help='Password')
    mysql_parser.add_argument('-U', '--userfile', type=argparse.FileType('r'), help='User File')
    mysql_parser.add_argument('-P', '--passfile', type=argparse.FileType('r'), help='Password File')

    # Directory subparser
    directory_parser = subparsers.add_parser('directory', help='Perform Directory Fuzzing')
    directory_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    directory_parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='Fuzzing File', required=False)
    directory_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    # Subdomain subparser
    subdomain_parser = subparsers.add_parser('subdomain', help='Perform Subdomain Fuzzing')
    subdomain_parser.add_argument('-T', '--target', type=str, help='Specify Target', required=True)
    subdomain_parser.add_argument('-F', '--file', type=argparse.FileType('r'), help='Subdomain file')
    subdomain_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # Handle each method
    if args.method == 'ftp':
        userfile = None if not args.userfile else args.userfile.name
        passwordfile = None if not args.passwordfile else args.passwordfile.name
        NexFTP.bruteFTP(args.target, userfile, passwordfile, args.user, args.password)

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
        passwordfile = None if not args.passfile else args.passfile.name
        NexMySql.connectMySQL(args.target, args.user, args.password, userfile, passwordfile)

    elif args.method == 'directory':
        NexDir.fuzz(args.target, args.file.name, args.verbose) if args.file else NexDir.fuzz(args.target, verbose=args.verbose)

    elif args.method == 'subdomain':
        filtered_target = NexSubD.filter_url(args.target)
        NexSubD.fuzz(filtered_target, args.file.name, args.verbose) if args.file else NexSubD.fuzz(filtered_target, verbose=args.verbose)

if __name__ == '__main__':
    main()