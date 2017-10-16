#!/usr/bin/env python
import util.checkpkg as checkpkg

import sys
import subprocess
import json
import pymysql.cursors
import pymysql

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

    parser.add_argument('-u', '--username', required=True,
	help='MySQL username')

    parser.add_argument('-p', '--password', required=True,
        help='MySQL password')

    parser.add_argument('-H', '--hostname', required=True,
        help='MySQL Server')

    parser.add_argument('-d', '--database', required=True,
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

    
    start_time = time.time()


    #Connect to database
    connection = pymysql.connect(host=args.hostname,
                             user=args.username,
                             password=args.password,
                             db=args.database,
                             cursorclass=pymysql.cursors.DictCursor)

try:

    with connection.cursor() as cursor:
        sql = "SELECT `name`, `address`, `display` FROM `hosts` WHERE `monitored`=1"
        cursor.execute(sql)
        hosts = cursor.fetchall()
finally:
    connection.close()

    for host in hosts:
	host = str(host)

	'''If your communities/versions vary, modify credentials here. I've used last_octet to do this determination
	        octets = host.split('.')
                last_octet = str(octets[3]).strip()
	   Otherwise, grab the data
	'''

        hostname = ''

        if ',' in host:
            hostname, host = host.split(',')

        data = snmpget_by_cl(host, credential, oids)

        '''TODO: clean up this logic...'''
        try:
            output = data['output'].split('\n')
            community = data['community']

	    hostname = output[0].strip('"')
            sysdesc = output[1].strip('"')
            sysobject = output[2].strip('"') 

        except:
            community = 'unknown'
            output = ''

            sysdesc = ''
            sysobject = ''
	
	v_match = vendor_match(numbers, sysobject)	

	if v_match:
	    vendor = v_match['o'].strip('"')
	else:
	    vendor = None
	    
	all_hosts[host] = { 
	    'community': community, 'snmp_version': credential['version'], 'hostname': hostname, 'sysdesc': sysdesc, 'vendor' : vendor }

	if debug:
	    print host, sysobject, all_hosts[host]

    print "\n"
    print("Discovery took %s seconds" % (time.time() - start_time))
    print "Writing data to config file. Please wait"

    outfile = compile_hosts(all_hosts, location)
    print "Wrote data to "+outfile

def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}
    '''Iterate through specified args and make sure input is valid. TODO: add more flags'''
    for k,v in vars(args).iteritems():
        if k == 'network':
	    network = v.split('/')[0]
	    if len(network) > 7:
	    	if is_valid_ipv4_address(network) is False:
		    check_flags['is_valid_ipv4_address'] = False
	    else:	
		check_flags['is_valid_ipv4_format'] = False
		
    last_idx = len(check_flags) - 1
    last_key = ''

    '''Find last index key so all the violated flags can be output in the next loop'''
    for idx, key in enumerate(check_flags):
	if idx == last_idx:
	    last_key = key
	
    for flag, val in check_flags.iteritems():
        if val is False:
	    sys.stderr.write("Check "+flag+" failed to validate your input.\n")
	    if flag == last_key:
		return False 

def compile_hosts(data, location):
    if location: 
	loc = location.lower()
        filename = 'hosts_'+loc+'.conf'
    else:
	filename = 'discovered_hosts.conf'

    f = open(filename, 'w')

    for ip, hdata in data.iteritems():
	hostvars = compile_hvars(hdata['sysdesc'])

	if not hdata['hostname']:
	    hostname = ip
	else:
	    hostname = hdata['hostname']

	host_entry = build_host_entry(hostname, str(ip), location, hdata['vendor'], str(hostvars))

	f.write(host_entry)

    f.close()

    return filename

def build_host_entry(hostname, ip, location, vendor, hostvars):
    host_entry = ( 'object Host "%s" {\n'
		   '  import "generic-host"\n'
		   '  address = "%s"\n'
		 ) % (hostname, ip)

    if location:
	host_entry += '  vars.location = "{0}"\n'.format(location)
    if vendor:
	host_entry += '  vars.vendor = "{0}"\n'.format(vendor)
    if hostvars: 
	host_entry += '  {0}\n'.format(hostvars)

    host_entry += '}\n'

    return host_entry
	
def compile_hvars(sysdesc):
    sys_descriptors = {
	'RouterOS': 'vars.network_mikrotik = "true"', 
	'Linux':'vars.os = "Linux"', 
	'APC Web/SNMP': 'vars.ups_apc = "true"', 
    }

    hostvars = ''

    '''Append hostvars based on sysDescr matches'''
    for match, var in sys_descriptors.iteritems():
	if match in sysdesc:
	    hostvars += var +'\n  '

    return hostvars


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
