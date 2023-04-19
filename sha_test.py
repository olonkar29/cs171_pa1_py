import hashlib

if __name__ == "__main__":
    m = hashlib.new('sha256')
    m.update(b"Hello")
    sha_hex = m.hexdigest()
    length = 256
    print(sha_hex)
    print(len(sha_hex))
    sha_bin = bin(int(sha_hex, 16))
    print(sha_bin)
    print(len(sha_bin))
