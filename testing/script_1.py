from datetime import datetime
import socket
version = "Version of script is 1.0"

def get_current_time():
	now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
	return now

def get_ip():
	# The AF_INET address family is the address family for IPv4.
	#create an INET, STREAMing socket, SOCK_DGRAM Supports unreliable connectionless datagram communication.
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
	local_ip_address = s.getsockname()[0]
	return local_ip_address