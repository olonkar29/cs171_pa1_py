# server.py
# this process accepts an arbitrary number of client connections
# it echoes any message received from any client to console
# then broadcasts the message to all clients
import socket
import threading

from os import _exit
from sys import stdout
from time import sleep

def get_user_input():
	while True:
		user_input = input()
		if user_input!="":
			print(user_input)
		else:
			# close all sockets before exiting
			in_sock.close()
			for sock in out_socks:
				sock[0].close()
			print("exiting program", flush=True)
			# flush console output buffer in case there are remaining prints
			# that haven't actually been printed to console
			stdout.flush() # imported from sys library
			# exit program with status 0
			_exit(0) # imported from os library

# simulates network delay then handles received message
def handle_msg(data, addr, conn):
	# decode byte data into a string
	data = data.decode()
	# echo message to console
	print(f"{addr[1]}: {data}", flush=True)
	try:
		conn.sendall(bytes(f"{addr[1]}: {data}", "utf-8"))
		print(f"echoed message to port {addr[1]}", flush=True)
	except:
		print(f"exception in echoing to port {addr[1]}", flush=True)
		# continue
	# broadcast to all clients by iterating through each stored connection
	# for sock in out_socks:
	# 	conn = sock[0]
	# 	recv_addr = sock[1]
	# 	# echo message back to client
	# 	try:
	# 		# convert message into bytes and send through socket
	# 		conn.sendall(bytes(f"{addr[1]}: {data}", "utf-8"))
	# 		print(f"sent message to port {recv_addr[1]}", flush=True)
	# 	# handling exception in case trying to send data to a closed connection
	# 	except:
	# 		print(f"exception in sending to port {recv_addr[1]}", flush=True)
	# 		continue

# handle a new connection by waiting to receive from connection
def respond(conn, addr):
	print(f"accepted connection from port {addr[1]}", flush=True)

	# infinite loop to keep waiting to receive new data from this client
	while True:
		try:
			# wait to receive new data, 1024 is receive buffer size
			data = conn.recv(1024)
		# handle exception in case something happened to connection
		# but it's not properly closed
		except:
			print(f"exception in receiving from {addr[1]}", flush=True)
			break
			
		# if client's socket closed, it will signal closing without any data
		if not data:
			# close own socket to client since other end is closed
			conn.close()
			print(f"connection closed from {addr[1]}", flush=True)
			break

		# spawn a new thread to handle message 
		# so simulated network delay and message handling don't block receive
		threading.Thread(target=handle_msg, args=(data, addr, conn)).start()

if __name__ == "__main__":
	# specify server's socket address
	# programatically get local machine's IP
	IP = socket.gethostname()
	# port 3000-49151 are generally usable
	PORT = 8080

	# create a socket object, SOCK_STREAM specifies a TCP socket
	in_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# allow reusing socket in TIME-WAIT state
	# socket will remain open for a small period of time after shutdown to finish transmission
	# which will say "socket already in use" if trying to use socket again during TIME-WAIT
	# when REUSEADDR is not set
	in_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# bind socket to address
	in_sock.bind((IP, PORT))
	# start listening for connections to the address
	in_sock.listen()

	# container to store all connections
	# using a list/array here for simplicity
	out_socks = []
	# spawn a new thread to wait for user input
	# so user input and connection acceptance don't block each other
	threading.Thread(target=get_user_input).start()

	# infinite loop to keep accepting new connections
	while True:
		try:
			# wait to accept any incoming connections
			# conn: socket object used to send to and receive from connection
			# addr: (IP, port) of connection 
			conn, addr = in_sock.accept()
		except:
			print("exception in accept", flush=True)
			break
		# add connection to array to send data through it later
		out_socks.append((conn, addr))
		# spawn new thread for responding to each connection
		threading.Thread(target=respond, args=(conn, addr)).start()
