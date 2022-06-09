#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

void menu(){
	system("/bin/sh");
}

void init(){
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(120);
}

int main(){
	init();
	char name[32];
	printf("Input Name : ");
	fgets(name,42,stdin);
	printf("Hello ");
	printf(name);
	return 0;
}