#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <seccomp.h>
#include <sys/prctl.h>

float ch[63];
FILE *numbers2[14];
float numbers[30];

float get_float(){
	char ch[100];
	read(0,ch,99);
	return atof(ch);
}

int get_int(){
	char ch[50];
	read(0,ch,49);
	return atoi(ch);
}

void fill_data(){
	char temp[50];
	write(1,"Number of missions: ",strlen("Number of missions: "));
	int x = get_int();
	if(x>64 || x<0)
		exit(0);
	for(int i = 0; i <= x ; i++){
		sprintf(temp,"Mission %d code: ",i);
		write(1,temp,strlen(temp));
		ch[i]=get_float();
	}


}
int check(char *ch){
	int nb = 0;
	for(int i = 0 ;i<strlen(ch) ; i++){
		if((ch[i]>=65 && ch[i]<=90) || ch[i] == '_')
			nb+=1;
	}
	return nb == strlen(ch);
}
void get_name(char *dest){
	char name[100];
	while(1){
		write(1,"You secret agent name: ",strlen("You secret agent name: "));
		read(0,name,99);
		char *ch = strchr(name,'\n');
		if(ch)
			*ch = 0;
		if(check(name)){
			strncpy(dest,name,strlen(name));
			return;
		}
		printf("Agent name %s ",name);
		putchar('\n');
	}
}


void sandbox(){
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(lseek), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(writev), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_load(ctx);
    return;
}

int main(){
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	sandbox();
	char note[0x100];
	char name[100];
	printf("CIA reporting platform\n");
	get_name(name);
	numbers2[0]=fopen("logged_users.txt","ab");
	fprintf(numbers2[0],"\n%s\n",name);
	fill_data();
	puts("Report:");
	read(0,note,0x100);
	note[0x100]=0;
		
	
	fwrite(note,sizeof note, 1,numbers2[0]);
	
	return 0;
}
//gcc task.c -l seccomp -g -Wl,-z,relro,-z,now -o main
