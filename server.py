# server.py
# this process accepts an arbitrary number of client connections
# it echoes any message received from any client to console
# then broadcasts the message to all clients
import socket
import threading
import hashlib


from os import _exit
from sys import stdout
from time import sleep

def get_user_input():
	while True:
		user_input = input()
		if user_input=="Blockchain":
			b.printBlockchain()
		elif user_input=="Balance":
			b.calc_all_balance()
		elif user_input[0:3] == "wai":
			# print(f"waiting {user_input[5:]} seconds",flush=True)
			sleep(int(user_input[5:]))
		elif user_input =="exit":
			# close all sockets before exiting
			in_sock.close()
			for sock in out_socks:
				sock[0].close()
			# print("exiting program", flush=True)
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
	# print(f"{addr[1]}: {data}", flush=True)
	# print(f"{data[0:4]}",flush=True)
	try:
		if data[0:4] == "Hell":
			# print(f"new client {data[6]}",flush=True)
			client_order.append(int(data[6]))
		elif data[0:3] == "Bal":
			balance = b.calc_balance(data[8:])
			conn.sendall(bytes(f"Balance: ${balance}","utf-8"))
		elif data[0:3] == "Tra":
			index = 0
			for i in range(len(client_order)):
				if out_socks[i][1][1] == addr[1]:
					index = i
			sender = "P" + str(client_order[index])
			# print(sender)
			receiver = data[9:11]
			# print(receiver)
			amount = int(data[13:])
			# print(amount)
			balance = b.calc_balance(sender)
			# print("a")
			if balance >= amount:
				# print("b")
				new_block = Block(sender, receiver, amount)
				b.addBlock(new_block)
				# print("c")
				conn.sendall(bytes(f"Success", "utf-8"))
				# print("d")
			else:
				conn.sendall(bytes(f"Insufficient Balance", "utf-8"))
		else:
			conn.sendall(bytes(f"{addr[1]}: {data}", "utf-8"))
			print(f"echoed message to port {addr[1]}", flush=True)
	except:
		print(f"exception in echoing to port {addr[1]}", flush=True)

# handle a new connection by waiting to receive from connection
def respond(conn, addr):
	# print(f"accepted connection from port {addr[1]}", flush=True)

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
			# print(f"connection closed from {addr[1]}", flush=True)
			break

		# spawn a new thread to handle message 
		# so simulated network delay and message handling don't block receive
		threading.Thread(target=handle_msg, args=(data, addr, conn)).start()



def sha256(input, format="hex"):
    h = hashlib.new('sha256')
    h.update(bytes(input, 'utf-8'))
    hex = h.hexdigest()
    if format=="bin":
        bin_val = "{0:b}".format(int(hex,16))
        # change hex string to binary
        return str(bin_val)
    elif format=="hex":
        return hex
    else:
        return "LAME"

def hex_to_binary(input):
    return str(bin(int(input, 16))[2:].zfill(256))

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def getSender(self):
        return self.sender
    
    def getReceiver(self):
        return self.receiver
    
    def getAmount(self):
        return self.amount
    
    def toString(self):
        return "(" + self.sender + "," + self.receiver + ",$" + str(self.amount) + ")" 
    
class Block:
    def __init__(self, sender, receiver, amount):
        self.transaction = Transaction(sender, receiver, amount)
        self.nonce = 0
        self.hash = ""
        self.pointer = 0
    
    def toString(self):
        return self.hash + self.transaction.getSender() + self.transaction.getReceiver() + "$" + str(self.transaction.getAmount()) + str(self.nonce)
    
    def toString_forNonce(self):
        return self.hash + self.transaction.getSender() + self.transaction.getReceiver() + "$" + str(self.transaction.getAmount())

    def toString_forChain(self):
        return "(" + self.transaction.getSender() + "," + self.transaction.getReceiver() + ",$" + str(self.transaction.getAmount()) +"," + self.hash + ")"

    def setHash(self, hash):
        self.hash = hash

    def setPointer(self, pointer):
        self.pointer = pointer
    
    def setNonce(self):
        self.nonce = 0
        
        while(True):
            h = sha256(self.toString_forNonce()+str(self.nonce),"hex")
            if (h[0] == '0' or h[0] == '1' or h[0] == '2' or h[0] == '3') :
                break
            else:
                self.nonce+=1
        # print(h)
        # print(self.nonce)
    
    def getHash(self):
        return self.hash
    
    def getNonce(self):
        return self.nonce

    def getPointer(self):
        return self.pointer

    def getTransaction(self):
        return self.transaction


class Blockchain:
    def __init__(self):
        self.chain = []
        self.num_transactions = 0
    
    def addBlock(self, block):
        if (self.num_transactions == 0) :
            block.setHash(("0"*64))
        else:
            prev_block = self.chain[self.num_transactions - 1].toString()
            # print(prev_block)
            block.setHash(sha256(prev_block, "hex"))
        block.setNonce()
        block.setPointer(self.num_transactions-1)
        self.chain.append(block)
        self.num_transactions+=1
    
    def printBlockchain(self):
        out = "["
        for i in range(self.num_transactions):
            out+=(self.chain[i].toString_forChain())
            if(i<self.num_transactions-1):
                out+=","
        out += "]"
        print(out)
    
    def calc_balance(self, client):
        balance = 10
        for i in range(self.num_transactions):
            transaction = self.chain[i].getTransaction()
            
            if (transaction.getSender() == client) :
                balance -= transaction.getAmount()
            elif (transaction.getReceiver() == client):
                balance += transaction.getAmount()
        return balance
    
    def calc_all_balance(self):
        balance = []
        balance.append(self.calc_balance("P1"))
        balance.append(self.calc_balance("P2"))
        balance.append(self.calc_balance("P3"))
        print('P1: $%d, P2: $%d, P3: $%d'%(balance[0],balance[1],balance[2]))




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

	b = Blockchain() 
	# container to store all connections
	# using a list/array here for simplicity
	out_socks = []
	client_order = []
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
