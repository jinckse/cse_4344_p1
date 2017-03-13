##@package server.py
# Simple HTTP server implementation.
# TODO: Scale HTTP messages and flesh out, start threading, and
# resolve error fall out after successful run
##@author Jarrod Nix

import socket
import os
import sys
import threading

#
# CONSTANTS
#

HOST = ''
MAX_PACKET = 1024
DEBUG = 0

try:
	PORT = sys.argv[1]
except:
	# Notify user
	print('Unknown option -- usage: server.py <port_no>')
	sys.exit(0)

#
# FUNCTIONS
#

## Used to launch new threads for each client
#
def clientThread(conn, addr):

	print('Hostname\t\t: ', addr[0])
	print('Socket family\t\t: ', conn.family)
	print('Socket type\t\t: ', conn.type)
	print('Socket protocol\t\t: ', conn.proto)
	print('Socket timeout\t\t: ', conn.gettimeout())
	print('Socket peer name\t: ', conn.getpeername())

	# Keep thread alive
	try:
		msg = conn.recv(MAX_PACKET)

		if DEBUG: print(msg)
		
		if msg: 
			filename = msg.split()[1]
			print('Server received request for file: ' + filename.decode('ascii'))
			location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(filename.decode('ascii')[1:])))

			f = open(os.path.join(location, filename.decode('ascii')[1:]))
			print('File opened successfully')

			outputData = f.read()
			
			print('Sending response to client')
			# Send one HTTP header line into socket
			conn.send(bytes("HTTP/1.1 200 OK\n"
				+"Content-Type: text/html\n"
				+"\n", 'ascii'))

			# Send contents of the requested file to the client
			for i in range(0, len(outputData)):
				conn.send(bytes(outputData[i], 'ascii'))

	except IOError:
		# Notify user
		conn.send(bytes("HTTP/1.1 404 Not Found\n"
			+"Content-Type: text/html\n"
			+"\n", 'ascii'))

	# Close socket
	print('Closing socket')
	conn.close()

#
# MAIN THREAD
# 

# Initialize socket
print('Initializing server')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket
try:
	s.bind((HOST, int(PORT)))

except socket.error as msg:
	print('Bind failed: ' + str(msg))
	sys.exit()

print('Socket bind successful')

# Start listening
s.listen(1)

print('Socket now lisetning on port', PORT)
print('Socket Host name: ' + socket.gethostname())

# Wait for clients
while 1:

	# Wait to accept a connection
	conn, addr = s.accept()
	print('--')
	print ('Connected with client', addr[0] + ':' + str(addr[1]))

	# Launch new thread
	print ('Launching new thread for client ', addr[0] + ':' + str(addr[1]))
	threading.Thread(None, clientThread(conn, addr)).start()

