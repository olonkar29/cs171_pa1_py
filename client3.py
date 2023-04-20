# client3.py
# this process only connects to a predefined server
# it sends any input it receives from the user to the server
# and echoes any message it receives from the server to console
import socket
import threading
import sys
from os import _exit
from sys import stdout
from time import sleep

# keep waiting and asking for user inputs
def get_user_input():
	while True:
		# wait for user input
		user_input = input()
		if user_input == "exit":
			# close socket before exiting
			out_sock.close()
			# print("exiting program")
			# flush console output buffer in case there are remaining prints
			# that haven't actually been printed to console
			stdout.flush() # imported from sys library
			# exit program with status 0
			_exit(0) # imported from os library
		elif user_input[0:4] == "wait":
			sleep(int(user_input[5:]))
		else:
			try:
				# send user input string to server, converted into bytes
				out_sock.sendall(bytes(user_input, "utf-8"))
			# handling exception in case trying to send data to a closed connection
			except:
				print("exception in sending to server")
				continue
				
			# print("sent latest input to server")

# simulates network delay then handles received message
def handle_msg(data):
	# decode byte data into a string
	data = data.decode()
	# echo message to console
	print(data)

if __name__ == "__main__":
	sleep(1)
	# specify server's socket address so client can connect to it
	# since client and server are just different processes on the same machine
	# server's IP is just local machine's IP
	SERVER_IP = socket.gethostname()
	SERVER_PORT = 8080

	# create a socket object, SOCK_STREAM specifies a TCP socket
	# do not need to specify address for own socket for making an outbound connection
	out_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# attempt to connect own socket to server's socket address
	out_sock.connect((SERVER_IP, SERVER_PORT))
	# print("connected to server")
	out_sock.sendall(bytes("Hello 3", "utf-8"))
	# spawn new thread to keep waiting for user inputs
	# so user input and socket receive do not block each other
	threading.Thread(target=get_user_input).start()

	# infinite loop to keep waiting to receive new data from server
	while True:
		try:
			# wait to receive new data, 1024 is receive buffer size
			# set bigger buffer size if data exceeds 1024 bytes
			data = out_sock.recv(1024)
		# handle exception in case something happened to connection
		# but it's not properly closed
		except:
			print("exception in receiving")
			break
		# if server's socket closed, it will signal closing without any data
		if not data:
			# close own socket since other end is closed
			out_sock.close()
			# print("connection closed from server")
			_exit(0)
			break

		# spawn a new thread to handle message 
		# so simulated network delay and message handling don't block receive
		threading.Thread(target=handle_msg, args=(data,)).start()
