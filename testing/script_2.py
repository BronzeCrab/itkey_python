import script_1 as sc_1

print sc_1.version
now = sc_1.get_current_time()
print now
my_ip = sc_1.get_ip()
print my_ip

print "Second variant of script - using classes"

# Classes with inheretence from object - python new-style classes.

class Date_and_ip(object):

	version = "Version of script is 1.0"

	def get_current_time(self):
		now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
		return now

	def get_ip(self):
		# The AF_INET address family is the address family for IPv4.
		#create an INET, STREAMing socket, SOCK_DGRAM Supports unreliable connectionless datagram communication.
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
		local_ip_address = s.getsockname()[0]
		return local_ip_address

class Child(Date_and_ip):
	def __init__(self):
		# In this variant it searches for global variable ( if i do just 'print version')
		# print version
		# But 'super' allows to connect to parent classes without explicit call of them
		print super(Child, self).version
		print super(Child, self).get_current_time()
		print super(Child, self).get_ip()

test = Child()
