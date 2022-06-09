#include<stdio.h>
#include<string.h>

//gcc -g -Wl,-z,relro,-z,now -no-pie soal.c -o soal
void init(){
	setvbuf(stdin, 0LL, 2, 0LL);
  	setvbuf(stdout, 0LL, 2, 0LL);
  	setvbuf(stderr, 0LL, 2, 0LL);
}

void cheat(long int pass1,long int pass2){
	printf("Oke, we have flag, but we need key\n");
	if (0x5045544952504153 == pass1 && pass2 == 0xdeadbeefdeadbeef){
		FILE *f = fopen("flag.txt", "r");
		char buf[50];
		if (f == NULL) {
		    printf("File doesn't exist\n");
		    // exit(1);
		}else{
			fgets(buf, 50, f);
			printf("Secret : %s",buf);
		}	
	}else{
		printf("You don't have key\n");
	}
}


void main(){
	init();
	char buff[40];
	int price;
	unsigned int money;
	printf("You have old laptop, then you want to sell it to buy flag\n");
	printf("How much do you want to sell your laptop ? ");
	scanf("%i",&price);
	if(price < 500 ){
		money=price;
		printf("OK you have %i$\n",money);
		if ( 100000 < money){
			printf("Sorry, flag isn't available right now\nYou can make note for owner : ");
			read(0,buff,104);
		}else{
			printf("But price for flag 100000$,so you cann't buy flag\n");
		}
	}else{
		printf("It's quite expensive\n");
	}
	// exit(1);
}