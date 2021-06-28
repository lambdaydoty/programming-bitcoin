import hashlib

def hash256(s):
    r1 = hashlib.sha256(s).digest()
    r2 = hashlib.sha256(r1).digest()
    return r2
