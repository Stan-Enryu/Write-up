#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

//gcc -g -Wl,-z,relro,-z,now -fstack-protector -no-pie soal.c -o soal
void print_flag(){
	FILE *f = fopen("flag.txt", "r");
	char buf[50];
	if (f == NULL) {
	    printf("File tidak bisa dibuka\n");
	    exit(1);
	}
	fgets(buf, 50, f);	
	printf("Secret : %s\n",buf);
	exit(1);
}

void init(){
	setvbuf(stdin, 0LL, 2, 0LL);
  	setvbuf(stdout, 0LL, 2, 0LL);
  	setvbuf(stderr, 0LL, 2, 0LL);
  	alarm(30);
}

void main()
{
	init();
	char nama[40];
	char cerita[64];

	printf("Masukan nama : ");
	read(0,nama,121);
	printf("Selamat datang %s",nama);
	printf("Ceritakan pengalaman kamu : ");
	read(0,cerita,96);
	if (strlen(cerita)< 20){
		printf("kurang panjang bro...\n");
	}else{
		printf("cerita kamu bagus sekali\n");
	}

}