# icinga-autod

##Purpose:
The purpose of icinga-autod is to bring basic auto-discovery (to Icinga2 or Nagios Core) in an effort to take some of the pain away from discovering and adding a bunch of devices on new or existing networks. The focus of this tool is to quickly generate a fairly suitable host config with custom vars to tie them to HostGroups. 

##Usage:
./icinga-autod.py -n 192.168.1.0/24 -l LOCATION

##TODO:
- Make host recognition more universal - like Vendor lookup based on sysObjectID OID
 - http://www.iana.org/assignments/enterprise-numbers/enterprise-numbers
 - Kind of like this: http://search.cpan.org/~endler/Net-SNMP-Vendor-0.01a/Vendor.pm
- Allow user to input hostname FQDN format (should it come to that)
- Allow different hostype definitions (maybe parse templates.conf)
- Allow more in-depth host objects in general
