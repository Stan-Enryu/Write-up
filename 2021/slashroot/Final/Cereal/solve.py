import gdb
import sys

cereal1 = '08498612420008497362530843487879'
cereal2 = '59136831783676475140286694187307'
cereal3 = '73396680181532725040642253521829'

gdb.execute('file ./cereal')
gdb.execute('b *0x555555401009')
gdb.execute('b *0x555555400ed1')
gdb.execute('r')

wait = input("Pause")

flag = ''
for i in range(32):
	gdb.execute('c')
	o = gdb.execute('x/bx $rbp-0x64', to_string=True)[:-1].split('\t')
	flag += chr(int(o[1],16))
	print(flag)

gdb.execute('c')
wait = input("Pause")

flag = ''
for i in range(32):
	gdb.execute('c')
	o = gdb.execute('x/bx $rbp-0x64', to_string=True)[:-1].split('\t')
	flag += chr(int(o[1],16))
	print(flag)

gdb.execute('c')

flag = ''
for i in range(32):
	gdb.execute('c')
	o = gdb.execute('x/bx $rbp-0x64', to_string=True)[:-1].split('\t')
	flag += chr(int(o[1],16))
	print(flag)

gdb.execute('c')

gdb.execute('quit')
