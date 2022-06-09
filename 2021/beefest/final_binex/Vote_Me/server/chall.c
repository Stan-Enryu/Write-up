#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char junk[0x700];
char name[88];
char command[8];
long int password=0;
void set_password(long int pass){
	password=pass;
	if (password==0xbeefe572021){
		strncpy(command,"/bin/sh\x00",8);
	}else{
		printf("Wrong password \n");
	}
}

void back(){
	if (password==0xbeefe572021){
		system(command);
	}else{
		printf("Wrong password \n");
	}
}

void init(){
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(120);
}

int main(){
	init();
	char number[64];
	printf("Presidential election\n");
	printf("Your name: ");
	fgets(name,80,stdin);
	printf("List Name President\n");
	printf("1. Bayu\n");
	printf("2. Ilham\n");
	printf("3. Bagus\n");
	printf("Choose number: ");
	fgets(number,80,stdin);
	return 0;
}