import string 
import base64
import base36 

def fun_1(b):
    return ''.join([chr((ord(i)-97-1-(1^2))%26+97) for i in b])

temp=base36.dumps(16166842727364078278681384436557013)

print 'COMPFEST12{' + fun_1(temp) + '}'