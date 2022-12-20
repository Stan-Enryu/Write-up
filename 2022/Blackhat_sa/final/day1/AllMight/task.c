#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>


int heroes_skills_size[20]={ 0 };
int chairs[20]={ 0 };
char *heroes[20]={ 0 };
int number_heroes=0;



void menu(){
	puts("1- Add hero to class");
	puts("2- Edit hero's skill");
	puts("3- Kick hero");
	puts("4- Look into hero's skill");
	puts("5- Exit");
	write(1,"> ",2);
}

int read_int(){
	char var[5];
	int size;
	read(0,var,4);
	size = atoi(var);
	return size;
}
void new_hero(){
	if(number_heroes >= 20)
	{
		puts("Class is full :(");
		return;
	}
	char var[20];
	long long int size;
	puts("Hero skill's description size:");
	read(0,var,20);
	size = atoll(var);
	
	for(int i = 0 ; i<20 ; i++){
		if(chairs[i] == 0){
			heroes[i] = (char *)malloc(size);
			chairs[i] = 1;
			heroes_skills_size[i] = size;
			printf("You got new hero at chair %d @ with location 0x%llx \n",i,heroes[i]);
			number_heroes = number_heroes + 1 ;
			break;
		}
	}
}
void edit_skill(){
	char var[5];
	int index;
	puts("Hero chair index:");
	read(0,var,4);
	index = atoi(var);
	if(index >=0 && index <=19){
		if(chairs[index]){
			puts("describe hero's skill:");
			int string_length=read(0,heroes[index],heroes_skills_size[index]);
			heroes[index][string_length]='\0';
		}
	}else{
		puts("Chair is empty!");
		return ;
	}
} 
void kick_hero(){
	char var[5];
	int index;
	puts("Hero chair index:");
	read(0,var,4);
	index = atoi(var);
	if(index >=0 && index <=19){
		if(chairs[index] == 0){
			puts("Chair is empty!");
			return ;
		}else{
			free(heroes[index]);
			chairs[index] = 0 ;
			number_heroes = number_heroes - 1;
		}
	}else{
		puts("Chair is in another classroom!");
		return ;
	}
}
void show_hero_skill(){
	char var[5];
	int index;
	puts("Hero chair index:");
	read(0,var,4);
	index = atoi(var);
	if(index >=0 && index <=19){
		if(heroes[index]){
			puts("skill description:");
			write(1,heroes[index],heroes_skills_size[index]);
		}
	}else{
		puts("Chair is empty!");
		return ;
	}
} 
int diary(){
	int choice;
	puts("Welcome to boku no hero academia");

	while(1){
		menu();
		choice = read_int();
		switch(choice){
			case 1:new_hero();break;
			case 2:edit_skill();break;
			case 3:kick_hero();break;
			case 4:show_hero_skill();break;
			case 5:return 0;
		}
	}
	
	return 0;
}
int main(){
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	diary();
	return 0;
}
//gcc -Wl,-z,norelro -o main task.c -no-pie 
