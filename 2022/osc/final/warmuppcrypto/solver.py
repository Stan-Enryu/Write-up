FLAG_ENC = "525843323032327b454145565849525f4658434a5456565f4147475f4342565f57444b455f5652534e417d".decode('hex')
KEY = 'SUPERSECRET'

def caesar_enc(p,k):
    cipher = ""
    for i in range(len(p)):
        if p[i].isalpha():
            cipher += chr(((ord(p[i]) - 65 - len(k)) % 26) + 65)
        else:
            cipher += p[i]
    return cipher 

def vigenere_enc(p,k):
    cipher = ""
    for i in range(len(p)):
        if p[i].isalpha():
            cipher += chr((ord(p[i]) - 65 - ord(k[i % len(k)]) - 65) % 26 + 65) 
        else:
            cipher += p[i]
    return cipher

print (FLAG_ENC)

plain = vigenere_enc(FLAG_ENC, KEY)
print(plain)

plain = caesar_enc(plain, KEY)
print(plain)