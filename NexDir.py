"""
This file is part of NexScan.

NexScan is free software: you can use it for personal and non-commercial purposes under the terms of the Custom License.

For commercial use, please contact Nexeo Security at business@nexeosecurity.tech.

NexScan is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Custom License for more details, located in the LICENSE file.
"""

import requests
import argparse

def fuzz(target, file = 'small.txt'):
    try:
        with open(file, 'r') as f:
            for word in f.readlines():
                word = word.strip()
                response = requests.get(target + '/' + word)
                if response.status_code == 200:
                    print(f'\033[92m [+]\033[0m Found: {target}/{word}')
                # else:
                #     print(f'\033[91m [-]\033[0m Not Found: {target}/{word}')
    except KeyboardInterrupt:
        print('\033[91m [-]\033[0m Detecting Keyboard Interrupt...Exiting...')
        exit(1)

