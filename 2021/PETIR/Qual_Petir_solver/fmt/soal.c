#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<unistd.h>
//gcc -g -Wl,-z,relro,-z,now -fstack-protector-all -no-pie soal.c -o soal

void init(){
	setvbuf(stdin, 0LL, 2, 0LL);
  	setvbuf(stdout, 0LL, 2, 0LL);
  	setvbuf(stderr, 0LL, 2, 0LL);
  	alarm(30);
}

char pass2[8]="BINUS11";
char name_file[]="fake.txt";

void cek(){
	if(strncmp("PETIR21",pass2,7) == 0){
		FILE *f = fopen(name_file, "r");
		char buf[50];
		if (f == NULL) {
		    printf("File tidak bisa dibuka\n");
		    exit(1);
		}
		fgets(buf, 50, f);
		printf("Secret : %s",buf);
	}
}

void main(){
	init();
	char buff[160];
	char pass1[16];
	printf("---Login---\n");
	printf("Username : ");
	fgets(buff,160,stdin);
	printf("Password : ");
	fgets(pass1,16,stdin);
	if(strncmp("passwd123",pass1,9) == 0){
		printf("Berhasil LOGIN sebagai Mahasiswa Binus\n");
		printf("Welcome ");
		printf(buff);
		cek();
	}else{
		printf("PASSWORD Salah\n");
	}
}