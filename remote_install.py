import paramiko 
import logging
from optparse import OptionParser
import re
import sys

PACKAGE = 'isc-dhcp-server'

usage = "How to use: %prog [options] HOST_IP USERNAME PASSWORD PORT"
# creating OptionParser instance with usage parameter
parser = OptionParser(usage)
# adding options to parser instance
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose")
# default value for verbose option will be false
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose")
# calling parse_args() method
(options, args) = parser.parse_args()

# checking number of arguments
if len(args) not in (3,4):
	parser.error("incorrect number of arguments") 

# checking arguments
# checking ip
# checking each octet, splitting by "."

HOST_IP = args[0]
count = 0
valid_octet = re.compile("^\d{1,3}$") 
for octet in HOST_IP.split("."):
	if not valid_octet.match(octet) or int(octet) > 255:
		parser.error("incorrect IP")
	count += 1
if count != 4:
	parser.error("incorrect IP")
# checking username
USERNAME = args[1]
#allowed [A-Za-z0-9_.-], may be $ at the end
valid_username = re.compile("^[\w\-\.]+\$?$") 
if not valid_username.match(USERNAME):
	parser.error("incorrect USERNAME")
# is it necessary to check password? I think no..
PASSWORD = args[2]
# checking PORT
if len(args) == 4:
	PORT = args[3]
	valid_port = re.compile("^\d{1,5}$") 
	if not valid_port.match(PORT) or int(PORT) > 2**16-1:
		parser.error("incorrect PORT")
# setting PORT to 22 if no argument	for it
else:
	PORT = 22
	if options.verbose:			
		print "assuming that PORT is 22"

print args    
print options
#using paramiko to connect to remote and install
client = paramiko.SSHClient()
#adding key of the server to known hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
	client.connect(hostname=HOST_IP, username=USERNAME, password=PASSWORD, port=PORT)
except paramiko.ssh_exception.AuthenticationException:
	parser.error("Failed to connect, check username")
except:
	parser.error("Failed to connect, check IP")
else:	
	stdin, stdout, stderr = client.exec_command('sudo -S apt-get -y install %s' % PACKAGE)
	stdin.write(PASSWORD + '\n')
	stdin.flush()
	print stdout.readlines()
	stdin, stdout, stderr = client.exec_command('apt-cache policy %s' % PACKAGE) 
	stdin.flush()
	check_if_installed = stdout.readlines()
	client.close()
	print check_if_installed
	#setting up logging
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
	#logging, checking if installed
	#it wasn't necessary but i've tried to generalize script for any package, not only apache2
	#so i'm checking if is there anything in check_if_installed string - don't understand,
	#but it is empty if i give random package name - stdout.readlines() doesn't return anything in this
	#case, don't know why
	if not check_if_installed:
		logging.error('Something gone wrong - probably bad package name, %s isn\'t installed' % PACKAGE)
		sys.exit()
	for phrases in check_if_installed:
		if 'Installed: (none)' in phrases:
			logging.error('Something gone wrong - probably no internet on remote, %s isn\'t installed' % PACKAGE)
			sys.exit()
	logging.info('Sucessfully installed')


