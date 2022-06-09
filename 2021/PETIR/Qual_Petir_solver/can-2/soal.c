#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

//gcc -g -Wl,-z,relro,-z,now -fstack-protector -no-pie soal.c -o soal
//gcc -g -Wl,-z,relro,-z,now -fstack-protector soal.c -o soal
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

void bug(){
	char cerita[80];
	char nama[40];
	printf("Masukan nama : ");
	fgets(nama, 40, stdin);
	printf("Selamat datang ");
	printf(nama);
	printf("Ceritakan pengalaman kamu : ");
	read(0,cerita, 106);
	if (strlen(cerita)< 20){
		printf("kurang panjang bro...\n");
	}else{
		printf("cerita kamu bagus sekali\n");
	}
}

void main(int argc, char const *argv[]){
	init();
	bug();
}