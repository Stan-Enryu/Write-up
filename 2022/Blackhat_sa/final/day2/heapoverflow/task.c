#include <stdio.h>
#include <string.h>
#include <stdlib.h>



struct Page {
   long long int function_address;
   char  page_content[0x100];
}; 

typedef int func(char *);

struct Page * page[2];

int mysterious_function(ch){
	system(ch);
	return 0;
}

int print_page(ch){
	write(1,ch,0x88);
	return 0;
}

int show_page(){
	puts("index:");
	int index= read_int();
	if (index != 0 && index!=1)
		return 0;

	func* f=(func*)page[index]->function_address;
	f(page[index]->page_content);
	return 0;
}

int renew_page(){
	puts("index:");
	int index = read_int();
	if (index != 0 && index!=1)
		return 0;
	page[index]=(struct Page*)malloc(0x88);
	page[index]->function_address=&print_page;
}

int edit_page(){
	puts("index:");
	int index = read_int();
	if (index != 0 && index!=1)
		return 0;
	puts("Please fill the page with data:");
	read(0,page[index]->page_content,0x100);
}

void menu(){
	puts("1- Get empty page");
	puts("2- Write to the page");
	puts("3- Show the page");
	puts("4- Exit");
	write(1,"> ",2);
}

int read_int(){
	char ch[10];
	int a;
	read(0,ch,8);
	a = atoi(ch);
	return a;
}


int main(){
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	int choice;
	while (1){
		menu();
		choice = read_int();
		switch(choice){
			case 1: renew_page(); break;
			case 2: edit_page();  break;
			case 3: show_page();  break;
			case 4: exit(0);
			default: break;
		}
	}

	return 0;
}

//gcc -o main task.c -no-pie