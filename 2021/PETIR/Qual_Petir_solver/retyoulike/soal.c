#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
//gcc -g -Wl,-z,relro,-z,now -no-pie -o soal soal.c
void flag(){

}

void sub_data(){
	char Alamat[40],HP[16],Motto[24],Tgllhr[16];

	printf("Tanggal lahir (hh-mm-yyyy):");
	fgets(Tgllhr,16,stdin);
	printf("Alamat : ");
	fgets(Alamat,120,stdin);
	printf("HP : ");
	fgets(HP,13,stdin);
	if(strlen(HP) != 12){
		exit(0);
	}
	printf("Motto Hidup : ");
	fgets(Motto,24,stdin);

}

void init(){
	
	setvbuf(stdin, 0LL, 2, 0LL);
  	setvbuf(stdout, 0LL, 2, 0LL);
  	setvbuf(stderr, 0LL, 2, 0LL);
  	alarm(30);

}

void main(){
	init();
	char buff[64];
	printf("---Data---\nName: ");
	fgets(buff,64,stdin);
	printf("Welcome %s",buff);
	sub_data();
	printf("Good bye %s",buff);
	exit(0);
}