#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <limits.h>

#define MAX 125
#define URANDOM_DEVICE "/dev/urandom"

static FILE *urandom;

int random_number(void) {
    int c;
    do {
        c = fgetc(urandom);
        if (c == EOF) {
            fprintf(stderr, "Failed to read from %s\n", URANDOM_DEVICE);
            exit(EXIT_FAILURE);
        }
    }
    while (c >= (UCHAR_MAX + 1) / MAX * MAX);

    return c % MAX;
}


int main(){
	urandom = fopen(URANDOM_DEVICE, "rb");
    if (urandom == NULL) {
        fprintf(stderr, "Failed to open %s\n", URANDOM_DEVICE);
        exit(EXIT_FAILURE);
    }

    char temp[10];
    for (int i = 0; i < 8; i ++) {
        temp[i] = random_number();
        if(temp[i]<=32){
            temp[i]+=32;
        }
    }
    fclose(urandom);

	char username[64];
	char *pass = temp;
	char *password_address[10];
	int comp;

	setbuf(stdin, NULL);
  	setbuf(stdout, NULL);
  	setbuf(stderr, NULL);

  	printf("WELCOME TO MAP ME\n");
  	printf("what's your name: ");
  	scanf("%20s", username);
  	printf("Hello ");
  	printf(username);
  	printf(" !!!\n");

  	printf("what is the secret? : ");
  	scanf("%20s", password_address);
  	comp = strncmp(password_address, pass, 10);
	if(comp == 0 ){
		system("cat flag.txt");
	}
	else{
		printf("wrong secret\n");
	}

}


