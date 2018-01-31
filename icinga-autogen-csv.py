#!/usr/bin/env python
import sys
import subprocess
import json
import csv

try:
    import argparse
except ImportError:
    checkpkg.check(['python-argparse'])

import time
import socket

"""

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

USAGE = './icinga-autogen.py --customer file.csv'

def build_parser():

    parser = argparse.ArgumentParser(description='Icinga2 config autogenerator - CSV')

    parser.add_argument('--customer', required=True,
	help='Customer string to use as prefix and template e.g., CUST-hostname (import CUST)')
    parser.add_argument('filename')

    return parser

def main():

    global debug

    parser = build_parser()
    args = parser.parse_args()

    '''Check arguments'''    
    if check_args(args) is False:
	sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
	sys.exit(1)

    '''Unknown function, I'll check it later''' 
    start_time = time.time()
    '''Reading host from csv'''
    read_hosts_from_csv(args.filename,args.customer)
def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def read_hosts_from_csv(data,customer):
    with open(data,'rb') as csvfile:    
        table = csv.DictReader(csvfile,delimiter=';')
        for row in table:
            if row['name']:
                print ('object Host "' + customer + "-" + row['name'].rstrip() + '" {')
                print ('import "' + customer + '"') 
                try:
                    del row['name']
                except KeyError:
                    pass
                print ('address = "' + row['ip'].rstrip() + '"') 
                try:
                    del row['ip']
                except KeyError:
                    pass
                for cell in row:
                    if cell:
                        if not (cell == 'model') and row[cell]:
                            print ('vars.' + cell + ' = "' + row[cell].replace('\n',' ') + '"')
                        elif row[cell]: 
                            print ('import "' + row[cell].replace('\n',' ') + '"')
                print ('}\n')
        return
	
def exec_command(command):
    """Execute command.
       Return a tuple: returncode, output and error message(None if no error).
    """
    sub_p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    output, err_msg = sub_p.communicate()
    return (sub_p.returncode, output, err_msg)


if __name__ == "__main__":
    main()
    sys.exit(0)
