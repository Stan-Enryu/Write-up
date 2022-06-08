import os
import subprocess
from pwn import xor
 
secret = b"z3solve_your_equation"
secret_int = int.from_bytes(secret, byteorder='big')
for i in range(4):
    secret_int >>= secret[i * 4]
    secret_int <<= secret[i * 4]
 
secret = secret_int.to_bytes(len(secret), 'big')
 
path = "./"
listOfFiles = subprocess.check_output(f'ls {path} | grep .pdf', shell=True).split(b'\n')[:-1]
 
signature = bytes.fromhex("255044462D")
for file in listOfFiles:
    content = open(f"{path}{file.decode()}","rb").read()[1337:-1337]
    secret2 = xor(content[:25], signature)[:len(secret)]
    rsecret = xor(secret, secret2)
   
    newContent = signature
    newContent += xor(content[25:], rsecret)
    open(f"decrypted_{file.decode()}","wb+").write(newContent)