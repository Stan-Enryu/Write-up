#include<stdio.h>
#include<unistd.h>
//gcc -Wl,-z,relro -no-pie -fstack-protector-all -o soal soal.c

void init(){
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);
    alarm(30);
}

void main(){
	char buff[100];
	char name[24];
	init();
	printf("Name : ");
	fgets(name,24,stdin);
	printf("Your Name : %s",name);
	printf("Note : ");
	read(0,buff,105);
	printf("Your Note: ");
	printf(buff);
}