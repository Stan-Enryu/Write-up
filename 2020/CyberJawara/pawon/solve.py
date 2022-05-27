from pwn import *
from z3 import *
import string
def check(c1,c2,c3):
	c3 + 2 * c1 == c2
data=string.ascii_letters + string.digits
print data

a1 = [BitVec(i, 8) for i in range(26)] 
s=Solver()
s.add( a1[5] == 45 )
s.add( a1[11] == 45) 
s.add( a1[18] == 45 )
s.add( a1[0] == a1[10] )
s.add( a1[1] == 101 ) # e
s.add( a1[3] == 80 ) # P
s.add( a1[25]== "\x00")
s.add( a1[2] == 109 ) # m
s.add( a1[4] == a1[1] )
s.add( a1[6] == 106 ) # j
s.add( a1[7] == 111 ) # o
s.add( a1[8] == a1[9] )
s.add( a1[9] == 83 ) # S
s.add( 9 + 2 * a1[5] == a1[12] )
s.add( a1[23] == a1[17] + 3 )
s.add( a1[13] == a1[20] )
s.add( a1[14] == 122 )
s.add( -134 + 2 * a1[15] == a1[16] )
s.add( a1[21] == 84 )
s.add( a1[16] == 72 )
s.add( a1[20] == 117 )
s.add( a1[17] == 53 )
s.add( a1[19] == 83 )
s.add( a1[22] == 49 )
s.add( a1[10] == a1[21] )
s.add( -61 + 2 * a1[24] == a1[20])

# check(a1[5], a1[12], 9) == 1 
# check(a1[15], a1[16], -134) == 1 
# check(a1[24], a1[20], -61) = 1 
s.check()
s.model()
l = [a1[i] for i in range(25)]
flag= [chr(s.model()[i].as_long()) for i in l ]
flag = ''.join(flag)
print flag

io=process("./pawon")
io.sendlineafter("> ","ribetmimi@gmail.com")
temp = flag+"\n"
# gdb.attach(io)
io.sendline(temp)
io.recvline()
print io.recvall()
# print io.recvline()

flag="r+jKctQn&m14l,.JBH8Wck\x14j"

# for i in range(200):
# 	temp=""
# 	for j in range(len(flag)):
# 		temp+=chr(ord(flag[j])+i)

# 	print temp

io.interactive()
