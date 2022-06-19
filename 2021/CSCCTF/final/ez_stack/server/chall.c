//gcc -g -Wl,-z,relro,-z,now -no-pie chall.c -o chall
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char buff_another[16];

void init(){
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(30);
}

void fun1(){
    char buff[8];
    write(1, "yow: ", 5);
    read(0, buff_another, 16);
    write(1, "yaharo: ", 8);
    read(0, buff, 24);
}

void main(){
	init();
	fun1();
}
