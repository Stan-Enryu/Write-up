import random
from collections import namedtuple
import gmpy2
from Crypto.Util.number import isPrime, bytes_to_long, inverse, long_to_bytes

# import string library function
import string

CHUNK_SIZE = 32
FLAG = b'FindITCTF{'+ b'a'*53 +b'}'

assert len(FLAG) % CHUNK_SIZE == 0
FLAG_CHUNKED = [FLAG[i:i+CHUNK_SIZE] for i in range(0, len(FLAG), CHUNK_SIZE)]
print (FLAG_CHUNKED)
assert len(FLAG_CHUNKED) == 2

PrivateKey = namedtuple("PrivateKey", ['b', 'r', 'q'])


def gen_private_key(size):
    s = 21120
    b = []
    for _ in range(size):
        ai = random.randint(s + 1, 2 * s)
        assert ai > sum(b)
        print(ai)
        b.append(ai)
        s += ai
    while True:
        q = random.randint(2 * s, 32 * s)
        if isPrime(q):
            break
    r = random.randint(s, q)
    # print (b)
    print('here')
    print (r)
    assert q > sum(b)
    assert gmpy2.gcd(q,r) == 1
    return PrivateKey(b, r, q)


def gen_public_key(private_key: PrivateKey):
    a = []
    for x in private_key.b:
        a.append((private_key.r * x) % private_key.q)
    return a


def encrypt(msg, public_key):
    assert len(msg) * 8 <= len(public_key)
    ct = 0
    print (len(msg)*8, len(public_key))
    msg = bytes_to_long(msg)

    print (hex(msg))
    for bi in public_key:
        ct += (msg & 1) * bi
        # print (msg & 1)
        msg >>= 1
    return ct


def decrypt(ct, private_key: PrivateKey):
    ct = inverse(private_key.r, private_key.q) * ct % private_key.q
    msg = 0
    for i in range(len(private_key.b) - 1, -1, -1):
         if ct >= private_key.b[i]:
             msg |= 1 << i
             ct -= private_key.b[i]
    return long_to_bytes(msg)

print (CHUNK_SIZE * 8)
print ('public_key')
private_key = gen_private_key(CHUNK_SIZE * 8)
print (private_key)

public_key = gen_public_key(private_key)
print ('encrypt')
# print (public_key)
encrypted = [encrypt(CHUNK, public_key) for CHUNK in FLAG_CHUNKED]
decrypted = [decrypt(CHUNK, private_key) for CHUNK in encrypted]
assert decrypted == FLAG_CHUNKED

print (decrypted)

for i in string.printable:
    print (bin(ord(i))[2:].rjust(8,"0"), i)
# print(f'public_key: {public_key}')
# print(f'encrypted: {encrypted}')
