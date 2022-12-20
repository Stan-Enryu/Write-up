#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>

char * notebook;
char *pages[5]={ 0 };
int pages_size[5];

void menu(){
	puts("1- New notebook");
	puts("2- Edit notebook");
	puts("3- Delete notebook");
	puts("4- Show notebook");
	puts("5- New page");
	puts("6- Edit page");
	puts("7- Delete page");
	puts("8- Show page");
	puts("9- Exit");
	write(1,"> ",2);
}

int read_int(){
	char kek[10];
	int size;
	read(0,kek,9);
	size = atoi(kek);
	return size;
}

void new_page(){
	puts("page size:");
	int page_size = read_int();
	if (page_size < 0x600){
		puts("NOPE!");
		return;
	}
	for(int i = 0 ; i<5 ; i++){
		if(pages[i] == 0){
			pages[i] = (char *)malloc(page_size);
			pages_size[i]=page_size;
			printf("You got new page at index %d\n",i);
			return;
		}
	}
	puts("Notebook is full!");
	return;
}

void edit_page(){
	int index;
	puts("Provide page index:");
	index = read_int();
	if(index >=0 && index <=4){
		if(pages[index]){
			puts("Provide new page content:");
			read(0,pages[index],pages_size[index]);
		}
	}else{
		puts("Wrong index!");
		return ;
	}
} 

void delete_page(){
	puts("Provide page index:");
	int index = read_int();
	if(index >=0 && index <=4){
		if(pages[index] == 0){
			puts("Deleted already!");
			return ;
		}else{
			free(pages[index]);
			pages[index] = 0 ;
			puts("DELETED!");
		}
	}else{
		puts("Wrong index!");
		return ;
	}
}

void show_page(){
	puts("Provide page index:");
	int index = read_int();
	if(index >=0 && index <=4){
		if(pages[index]){
			printf("OUTPUT:%s\n",pages[index]);
		}
	}else{
		puts("Wrong index!");
		return ;
	}
}

void new_notebook(){
	notebook=malloc(0x2000);
	puts("Allocated!");

	return;
}

void edit_notebook(){
	if (notebook){
		puts("Content:");
		read(0,notebook,0x2000);
	}else{
		puts("Not allocated!");
	}
	return;
}

void delete_notebook(){
	if (notebook){
		free(notebook);
		puts("Freed!");
	}else{
		puts("Already freed!");
	}
	return;
}

void show_notebook(){
	if (notebook){
		printf("OUTPUT: %s\n",notebook);
	}else{
		puts("Not allocated!");
	}
	return;
}


int secrets(){
	int choice;
	puts("Hey!");

	while(1){
		menu();
		choice = read_int();
		switch(choice){
			case 1:new_notebook();break;
			case 2:edit_notebook();break;
			case 3:delete_notebook();break;
			case 4:show_notebook();break;
			case 5:new_page();break;
			case 6:edit_page();break;
			case 7:delete_page();break;
			case 8:show_page();break;
			case 9:return 0;
		}
	}
	
	return 0;
}
int main(){
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);

	secrets();
	return 0;
}
// gcc -o main task.c