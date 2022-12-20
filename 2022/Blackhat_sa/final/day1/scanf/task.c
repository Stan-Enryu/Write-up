#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char * get_secret(char * secret){
	FILE *ptr = fopen("secret.txt", "r");
	if (NULL == ptr) {
        printf("file can't be opened \n");
        exit(0);
    }

    fgets(secret,63,ptr);
	return secret;
}

int main(){
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	int number1;
	int number2=0x38;
	char input[64];
	char secret[64];
	puts("Getting the secret..");
	strcpy(get_secret(secret),secret);
	puts("Here is a stack view for you.");
	write(1,input,number2);
	puts("\nGive me your lucky number:");
	scanf("%lld",&number1);
	puts("And another one!");
	write(1,input,number2);
	puts("Give me your wish:");
	read(0,input,64);
	if (strcmp(input,secret) == 0){
		puts("Wish granted!");
		system("/bin/sh");
	}else{
		puts("Maybe another time :) ");
	}
	
	return 0;
}

//gcc -o main task.c