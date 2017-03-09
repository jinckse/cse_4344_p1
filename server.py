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
PORT = sys.argv[1]
MAX_PACKET = 1024

#
# FUNCTIONS
#

## Used to launch new threads for each client
#
# TODO: Needs testing
def clientThread(conn):

	# Send welcome message
	conn.send(bytes('Server says: Welcome', 'ascii'))

	# Keep thread alive
	while 1:
		# Receive requests from client
		data = conn.recv(MAX_PACKET)
		reply = 'OK...' + str(data)
		
		if not data:
			break

		conn.sendall(bytes(reply, 'ascii'))

	# Broke from loop - close socket
	conn.close()

#
# MAIN THREAD
# 

# Initialize socket
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
print('Socket Host name: ' + socket.gethostbyname(socket.getfqdn()))

# Wait for clients
while 1:

	# Wait to accept a connection
	conn, addr = s.accept()
	print ('Connected with ', addr[0] + ':' + str(addr[1]))

	#Start new thread
	#print ('Launching new thread for client,', addr[0] + ':' + str(addr[1]))
	#threading.Thread(None, clientThread(conn), (conn,)).start()

	try:
		msg = conn.recv(MAX_PACKET)
		print(msg)
		
		if not msg:
			conn.send(bytes('Something went wrong', 'ascii'))

		filename = msg.split()[1]
		print('Server received request for file: ' + filename.decode('ascii'))
		location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(filename.decode('ascii')[1:])))

		f = open(os.path.join(location, filename.decode('ascii')[1:]))
		print('File opened successfully')

		outputData = f.read()

		# Send one HTTP header line into socket
		conn.send(bytes("HTTP/1.1 200 OK\n"
         +"Content-Type: text/html\n"
         +"\n", 'ascii'))

		# Send contents of the requested file to the client
		for i in range(0, len(outputData)):
			conn.send(bytes(outputData[i], 'ascii'))

		# Close socket
		print('Closing socket')
		s.close()

	except IOError:
		# Notify user
		conn.send(bytes("HTTP/1.1 404 Not Found\n"
         +"Content-Type: text/html\n"
         +"\n", 'ascii'))

		# Close socket
		print('Closing socket')
		s.close()

