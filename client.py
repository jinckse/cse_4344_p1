##@package client.py
# Simple HTTP client implementation.
##@author Jarrod Nix
import socket
import sys
import time

#
# CONSTANTS
#

# Populate user args
try:
	HOST = sys.argv[1]
	PORT = sys.argv[2]
	FILE = sys.argv[3]
except:
	# Notify user
	print('Unknown option -- usage: client.py <server_IPaddress> <port_no> <requested_file_name>')
	sys.exit(0)

#
# VARIABLES
#

msg = ''
rtt_start = time.clock()
rtt_stop = 0
rtt = 0

# Set up socket
print('Initializing client')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Connecting to remote host ' + HOST + ':' + PORT)

try:
	s.connect((HOST, int(PORT)))

	print('Hostname\t\t: ', HOST)
	print('Socket family\t\t: ', s.family)
	print('Socket type\t\t: ', s.type)
	print('Socket protocol\t\t: ', s.proto)
	print('Socket timeout\t\t: ', s.gettimeout())
	print('Socket peer name\t: ', s.getpeername())

	# Send message
	print('Sending request to host for file: ' + FILE)
	s.send((bytes("GET /" + FILE + " HTTP/1.1\n"
		+"\n", 'ascii')))

	# Gather reply
	while(1):
		data = s.recv(1024)

		if(data):
			data = data.decode('ascii')
			msg = msg + data
		else:
			print('Host replied: ')
			print(msg)

			rtt_stop = time.clock()
			rtt = (rtt_stop - rtt_start) * 1000
			rtt = round(rtt, 3)
			
			print('RTT: ' + str(rtt) + 'ms')

			print('Closing socket')
			s.close()
			break;

except:
	print('Connection to remote host ' + HOST + ' failed')
	print('Closing socket')
	s.close()

print('--')
