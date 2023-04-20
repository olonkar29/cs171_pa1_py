import hashlib

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
    # t = Transaction("P1", "P3", 3)

    b = Block("P1", "P2", 1)
    c = Blockchain()
    c.addBlock(b)
    c.printBlockchain()
    d = Block("P2", "P3", 9)
    c.addBlock(d)
    c.printBlockchain()
    c.calc_all_balance()
    