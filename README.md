# icinga2-gen

##Purpose:
The purpose of icinga2-autogen is to bring basic auto-generation of config files for Icinga2 by retrieving information from a iTop database.

##Installation
```bash
git clone https://github.com/hobbsh/icinga2-autod.git
cd icinga2-autod

./icinga-autod.py -n 192.168.1.0/24
```
Will output discovered_hosts.conf to current directory. 

##Usage:
This utility is meant to serve as a way to quickly generate a base hosts config for a given network. The host objects it creates (depending on the information it can gather) provide enough data to use HostGroups to do most of your check manangement. It's by no means a catch-all or the only way to do it, but I figured people might have a use for it.

```
usage: icinga-autod.py [-h] -n NETWORK [-L LOCATION] [-c COMMUNITIES]
                       [-d DEBUG]

required arguments
  -n NETWORK, --network NETWORK
                        Network segment to iterate through for live
                        IP addresses in CIDR IPv4 Notation (accepts single IPv4 address too)
optional arguments:
  -h, --help            show this help message and exit
  -L LOCATION, --location LOCATION
                        Location alias of the network - will be appended to
                        the hosts config (i.e. hosts_location.conf)
  -c COMMUNITIES, --communities COMMUNITIES
                        Specify comma-separated list of SNMP communities to
                        iterate through (to override default public,private)
  -d DEBUG, --debug DEBUG
			Use '-d True' to turn debug on
```
Add your own sys_descriptor matches in the compile_hvars method to add custom variables. Hoping to add a better way of handling this soon

##TODO:
- More options
 - Allow user to input hostname FQDN format (should it come to that)
 - Specify SNMP timeout/retries
- Allow different hostype definitions (maybe parse templates.conf)
- Allow more in-depth host objects in general
- Integrate with icingaweb2
- Add SNMPv3 Support
- Handle bad user input better
