import socket
hostname = socket.gethostname()
s1 = 'HOSTNAME:'
print(s1, hostname)

import getpass
username = getpass.getuser()
s2 = 'USERNAME:'
print(s2,username)

import os
homedir = os.environ['HOME']
s3 = 'HOME DIRECTORY:'
print(s3,homedir)

