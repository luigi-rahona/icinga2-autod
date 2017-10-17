# icinga2-autogen

# Purpose:
The purpose of icinga2-autogen is to bring basic auto-generation of config files for Icinga2 by retrieving information from a MySQL database; originally from an idea by hobbsh, whose code is partially included here.

# Installation
```bash
git clone https://github.com/luigi-rahona/icinga2-autogen.git
cd icinga-autogen

./icinga-autogen.py --username MySQL_user --password MySQL_password --hostname MySQL_server --database MySQL_database
```
will output itop-hosts.conf to current directory. 

# Usage:
Run icinga-autogen with MySQL credentials; the program is meant to be used with a software writing host information in a MySQL database, such as iTop.

The program currently imports information from a three-column table, featuring the following information:

- name: hostname;
- address: host ip;
- display: a short description of the host (e.g. displayed by external interfaces instead of the name if set).

potentially including all information employed by an Icinga2 host object, as described in (https://www.icinga.com/docs/icinga2/latest/doc/09-object-types/#host).
