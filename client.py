# Echo client
import socket
import sys

# Populate user args
HOST = sys.argv[1]
PORT = sys.argv[2]
FILE = sys.argv[3]

# Set up socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, int(PORT)))

# Send message
s.sendall( bytes('Client says: Hello world', 'ASCII') )

# Gather reply
while(1):
	data = s.recv(1024)

	if(data):
		data = data.decode('ascii')
		print('Received: ', data)
	else:
		s.close()
		break;

