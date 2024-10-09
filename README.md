# NexScan

[![License](https://img.shields.io/badge/license-Custom%20License-blue.svg)](./LICENSE)

## Description

NexScan: Penetration Testing Swiss Knife.
NexScan is a penetration testing tool designed to automate various tasks and provide a comprehensive set of features, which include Sub Domain Fuzzing, Directory Fuzzing, SSH Bruteforce, FTP Bruteforce, MySQL Bruteforce and SMB Bruteforce. The current version of the project i.e., NexScan v1.0.0 is a command line based tool.

## Usage

### Installation

### Setup

### Functionality

#### Directory Fuzzing
'''./NexScan.py directory -T https://nexeosecurity.tech'''

#### Sub-domain Fuzzing
```./NexScan.py subdomain -T https://nexeosecurity.tech```

#### SMB Enumeration
```./NexScan.py smb -T 172.16.173.148 -u kali -P unix_passwords.txt```

#### SSH Bruteforce
```./NexScan.py ssh -T 172.16.173.148```

#### FTP Bruteforce
```./NexScan.py ftp -T 172.16.173.148```

#### MySQL Bruteforce
```./NexScan.py mysql -T 172.16.173.148 -U unix_users.txt -p admin -v```

## License

This project is licensed under the terms of the [Custom License](./LICENSE).

For personal and non-commercial use only. For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

## Contributions

We welcome contributions! By contributing to this project, you agree that your contributions will be licensed under the same terms as the project.
