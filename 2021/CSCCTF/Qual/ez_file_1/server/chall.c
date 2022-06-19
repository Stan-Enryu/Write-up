#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <seccomp.h>

char *name_list;
int size=0;
int times=0;

void setup_seccomp(){
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(openat),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(read),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(write),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(mmap),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(getdents),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit_group),0);
	if(seccomp_load(ctx) < 0) exit(-1);
}

int readint(){
    char buf[0x9];
    return atoi(fgets(buf,0x9,stdin));
}

void edit(){
    int start=0;
    if (name_list != NULL && (0 <= times && times < 3)){
        printf("Start at : ");
        start = readint();
        if (start > 0){
            printf("Change name to : ");
            read(0,(long int*)(name_list+start),40);
            times++;
        }else{
            printf("error\n");
        }
    }else{
        printf("error\n");
    }
}

void add(){
    if (name_list == NULL){
        printf("Size name: ");
        size = readint();
        if (size > 0){
            name_list = (char*)malloc(size);
            if (!name_list){
                printf("error\n");
            }else{
                printf("Name : ");
                read(0, name_list, size);
            }
        }else{
            printf("error\n");
        }
    }else{
        printf("error\n");
    }
}

void init(){
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(60);
}

void menu(){
    printf("Blacklist Name\n");
    printf("Menu:\n");
    printf("1. Add Name.\n");
    printf("2. Edit Name.\n");
    printf("> ");
}

int main(){
    init();
    int number=0;
    setup_seccomp();
    memset(&name_list, 0, 8);
    while(1){
        menu();
        number = readint();
        if (number == 1){
            add();
        }else if(number == 2){
            edit();
        }else{
            printf("invalid number\n");
            break;
        }
    }
    return 0;
}
