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
    
if __name__ == "__main__":
    t = Transaction("P1", "P2", 5)
    print(t.getSender())
    print(t.getReceiver())
    print(str(t.getAmount()))
    print(t.toString())