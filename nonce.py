import hashlib

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
    

def getNonce(input):
    nonce = 0
    
    while(True):
        h = sha256(input+str(nonce),"hex")
        if (h[0] == '0' or h[0] == '1' or h[0] == '2' or h[0] == '3') :
            break
        else:
            nonce+=1
     
    return nonce

if __name__ == "__main__":
    # input = "Hello World"
    # print(sha256(input, "hex"))
    # input = "xys"
    # print(sha256("0000000000000000000000000000000000000000000000000000000000000000P1P3$30", "hex"))
    # print("3e2bab0d4b8ed142b634bcd47c7fe9fe09c66c4c94ca4891a526ed7ad66e3919")
    input = "0000000000000000000000000000000000000000000000000000000000000000P1P3$3"
    nonce = str(getNonce(input))
    print(sha256(input+nonce, "hex"))