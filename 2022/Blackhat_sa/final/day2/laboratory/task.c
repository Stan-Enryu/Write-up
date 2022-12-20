#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>

int page_size=0x100;
int check_pages[5]={ 0 };
char *pages[5]={ 0 };
int number_pages=0;



void menu(){
	puts("1- New test result");
	puts("2- Edit test result");
	puts("3- Delete test result");
	puts("4- Show test result");
	puts("5- Exit");
	write(1,"> ",2);
}

int read_int(){
	char kek[5];
	int size;
	read(0,kek,4);
	size = atoi(kek);
	return size;
}
void new_test(){
	if(number_pages >= 5)
	{
		puts("You can't have that much storage :(");
		return;
	}

	for(int i = 0 ; i<5 ; i++){
		if(check_pages[i] == 0){
			pages[i] = (char *)malloc(page_size);
			check_pages[i] = 1;
			printf("You got new test at index %d\n",i);
			number_pages = number_pages + 1 ;
			break;
		}
	}
}

void edit_test(){
	int index;
	puts("Provide test index:");
	index = read_int();
	if(index >=0 && index <=4){
		if(pages[index]){
			puts("Provide new test result:");
			read(0,pages[index],page_size);
		}
	}else{
		puts("Wrong index!");
		return ;
	}
} 

void delete_test(){
	char kek[5];
	int index;
	puts("Provide test index:");
	read(0,kek,4);
	index = atoi(kek);
	if(index >=0 && index <=4){
		if(check_pages[index] == 0){
			puts("Deleted already.");
			return ;
		}else{
			free(pages[index]);
			check_pages[index] = 0 ;
			number_pages = number_pages - 1;
			puts("DELETED!");
		}
	}else{
		puts("Wrong index!");
		return ;
	}
}
void show_test(){
	int index;
	puts("Provide test index:");
	index = read_int();
	if(index >=0 && index <=4){
		if(pages[index]){
			printf("OUTPUT:%s\n",pages[index]);
		}
	}else{
		puts("Wrong index!");
		return ;
	}
}
int laboratory(){
	int choice;
	puts("Welcome to the Laboratory!");

	while(1){
		menu();
		choice = read_int();
		switch(choice){
			case 1:new_test();break;
			case 2:edit_test();break;
			case 3:delete_test();break;
			case 4:show_test();break;
			case 5:return 0;
		}
	}
	
	return 0;
}
int main(){
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	srand((unsigned int) time(NULL));
	int i;
	int rand_number=(int)rand();
	rand_number=rand_number%100;

	for (i=0;i<rand_number;i++){
		int rand_size=(int)rand();
		rand_size=250 + (rand_size % 100);
		malloc(rand_size);
	}
	laboratory();
	return 0;
}
// gcc -o main task.c