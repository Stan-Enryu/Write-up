#include <stdio.h>
#include <string.h>
#include <stdlib.h>


char bb[256];
char aa[256];
char cc[256];


int validate_name_admin(){
	char secret_name[64];
	FILE *ptr = fopen("secret_name.txt", "r");
	if (NULL == ptr) {
        printf("file can't be opened \n");
        exit(0);
    }

    fgets(secret_name,64,ptr);
    if (strcmp(secret_name,aa) != 0){
    	strcpy(cc,"student");
    }

	return 0;
}

int main(){
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	puts("Welcome to the school system! \\o/");
	puts("Please provide your name:");
	scanf("%64s",aa);
	validate_name_admin();
	printf("Hey, %s \nWhat do you want to report?\n",aa);
	scanf("%256s",bb);
	printf("REPORT SAVED!\n");

	if (!strcmp(cc, "")){
		puts("Admin detected! connecting to the server..");
		system("/bin/sh");
	}
	return 0;
}

//gcc -o main task.c