import hashlib
import string
import random

def sha256(input, format="bin"):
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
        self.nonce = ""
        self.hash = ""
        self.pointer = 0
    
    def toString(self):
        return self.hash + self.transaction.getSender() + self.transaction.getReceiver() + "$" + str(self.transaction.getAmount()) + self.nonce
    
    def setNonce(self):
        while(True):
            # print(self.nonce)
            h = sha256(self.toString())
            print(h)
            if(h[0] == '0'):
                break
            else:
                if (len(self.nonce) > 200):
                    self.nonce = ""
                self.nonce += random.choice(string.ascii_letters)




# class Blockchain:
#     def __init__(self):
#         self.chain = []
#         self.num_transactions = 0
    
#     def addBlock(self):
#         if (self.num_transactions == 0) :
#             self.num_transactions += 1

    
if __name__ == "__main__":
    t = Transaction("P1", "P2", 5)
    print(t.getSender())
    print(t.getReceiver())
    print(str(t.getAmount()))
    print(t.toString())

    b = Block("P1", "P2", 5)
    print(b.toString())
    b.setNonce()
    print(b.toString)
    