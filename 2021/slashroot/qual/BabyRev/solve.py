import os

def shuffle_secret():
  secret_out = ''
  secret_str = ''.join('slarootshrrootootrootctfroot2021'.split("root"))
  for count, loop in enumerate(secret_str):
    if count % 2 == 0:
      secret_out += ''.join([chr(ord(ch) + 0x3) for ch in loop])
    else:
      secret_out += loop
  return secret_out

for root, dirs, files in os.walk("./secrets"):
  for file in files: 
    print (file)
    readFile = open("./secrets/"+file, "rb").read()

    enc = ''.join([chr((((a  - ord("S") - ord("L") - ord("A")- ord("S")- ord("H")- ord("R")- ord("O")- ord("O")- ord("T"))^ ord(b)))%256) for a, b in zip(readFile, shuffle_secret() * 25000)])

    open("./final/"+file, "wb").write(bytes(enc,"latin-1")) 

# Slashroot5{its_just_an_ez_chall}