#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


void buy_flag(){
	system("cat flag.txt");
}

void vuln(){
	char buffer[128];
	printf("please input a feedback\n");
	scanf("%s", buffer);
	printf("Thanks for the feedback!\n");
}

int main(){
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
  	setbuf(stderr, NULL);
	int saldo = 100;
	int menu = 0;
	char get_menu[4];
	while (1){
		int temp;
		printf("welcome to bybe ROP\n");
		printf("your balance: $%d\n", saldo);
		printf("1. withdraw money\n");
		printf("2. Buy flag($100099)\n");
		printf("3. feedback\n");
		printf("4. exit\n");
		printf("choose: \n");

		scanf("%1s", &get_menu);
		fflush(stdin);

		

			if (*get_menu == '1'){
				printf("please how much money to with draw: ");
				scanf("%d", &temp);
				if(temp > saldo){
					printf("not enough balance\n");
				}
				else{
					 saldo = saldo - temp;
					printf("balance updated!\n");
				}
			}
				

			else if(*get_menu == '2'){
				if(saldo > 100099){
					buy_flag();
				}
				else{
					printf("not enough money!\n");
				}
			
			}
				

			else if(*get_menu == '3'){
				vuln();

			}
				

			else if(*get_menu == '4'){
				exit(0);
			}
				
		

			else{
				printf("only 1-4\n");
			}
				
				
	}// while
	

}// main