//gcc -g -Wl,-z,relro,-z,now -no-pie soal.c -o soal
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char buff_another[100];

void fun1(){
    char buff[32];
    printf("Like Echo Command\n> ");
    read(0, buff, 41);
    printf("No Output\n");
}

void init(){
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(30);
}

void ent1(){
	fun1();
}

void main(){
	init();
	ent1();

}

void tools(){
    char buff[32];
    write(1, "You want use a tool (yes/no): ", 30);
    read(0, buff_another, 104);
    printf("What tool you want to use: \n");
    read(0, buff, 64);
}
