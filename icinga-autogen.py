#!/usr/bin/env python
import sys
import subprocess
import json
import pymysql.cursors

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

USAGE = './icinga-autogen.py -u mysql_username -p mysql_password -H mysql_host -d mysql_db'

def build_parser():

    parser = argparse.ArgumentParser(description='Icinga2 config autogenerator')

    parser.add_argument('--username', required=True,
	help='MySQL username')

    parser.add_argument('--password', required=True,
        help='MySQL password')

    parser.add_argument('--hostname', required=True,
        help='MySQL Server')

    parser.add_argument('--database', required=True,
        help='MySQL Database')
        
        
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
    '''Connect to db and grab hosts'''
    hosts = connect_db(args.hostname,args.username,args.password,args.database)

    '''Write the Icinga2 configuration file'''
    outfile = compile_hosts(hosts)
    '''All done'''
    print ("Wrote data to "+outfile+", it took --- %s seconds ---" % (time.time() - start_time))
def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def connect_db(hostname,username,password,db):
    #Connect to database
    connection = pymysql.connect(host=hostname,
                       user=username,
                       password=password,
                       db=db,
                       cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `name`, `address`, `display`, `template`, `place` FROM `hosts` WHERE `monitored`=1"
            cursor.execute(sql)
            hosts = cursor.fetchall()

    finally:
        connection.close()
        return hosts

def compile_hosts(data):
    filename = 'itop-hosts.conf'

    f = open(filename, 'w')

    for host in data:
        hostname = host["name"]
        ip = host["address"]
        display = host["display"]
        template = host["template"]
        group = host["place"]
	host_entry = build_host_entry(hostname, template, str(ip), display, group)
	f.write(host_entry)

    f.close()

    return filename

def build_host_entry(hostname, template, ip, display, group):
    host_entry = ( 'object Host "%s" {\n'
		   '  import "%s"\n'
		   '  address = "%s"\n'
                   '  display_name = "%s"\n'
                   '  groups = "[\"%s\"]"\n'
		 ) % (hostname, template, ip, display, group)

    host_entry += '}\n'

    return host_entry
	
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
