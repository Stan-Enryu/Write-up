# uncompyle6 version 2.11.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Apr 20 2020, 20:30:41) 
# [GCC 9.3.0]
# Embedded file name: script.py
# Compiled at: 2021-08-07 08:34:05
import zlib
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
public_key = '-----BEGIN PUBLIC KEY-----\nMCwwDQYJKoZIhvcNAQEBBQADGwAwGAIRAp6i5d8BDOZL/fbsZtrTB6kCAwEAAQ==\n-----END PUBLIC KEY-----'

def encrypt_key(aes_key, rsa_key):
    return pad_key(long_to_bytes(pow(bytes_to_long(aes_key), rsa_key.e, rsa_key.n)))


def pad_key(key):
    return key + chr(69) * (20 - len(key))


def compress_dir():
    return zlib.compress(''.join([ open(file_name).read() for file_name in filter(os.path.isfile, os.listdir(os.curdir)) ]))


def encrypt(data, aes_key, rsa_key):
    cipher = AES.new(aes_key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext = cipher.encrypt(data)
    return 'slyt' + nonce + encrypt_key(aes_key, rsa_key) + ciphertext


if __name__ == '__main__':
    out = open('slythereda', 'wb')
    out.write(encrypt(compress_dir(), os.urandom(16), RSA.import_key(public_key)))
    out.close()
# okay decompiling temp.pyc

# 504338478656760805506582215261851719625203212268109032551208024948
# 484338478656760805506582215261851719625203212268109032551208024948
# 494338478656760805506582215261851719625203212268109032551208024948
# 104338478656760805506582215261851719625203212268109032551208024948
# 359338478656760805506582215261851719625203212268109032551208024948
# 956533286609978570864513372183333576670807227231857802319196972847