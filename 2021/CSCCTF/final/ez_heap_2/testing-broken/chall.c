//gcc -g -Wl,-z,relro,-z,now chall.c -fstack-protector-all -o chall
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <seccomp.h>

void setup_seccomp(){
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(openat),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(read),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(write),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(mmap),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(lseek),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(getdents),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit_group),0);
    if(seccomp_load(ctx) < 0) exit(-1);
}

struct note {
    char* addr_note;
    size_t size;
};

struct name {
    char* addr_name;
    size_t size;
};

struct name name_list[8];
struct note note_list[2];
int count_name=0;
int count_note=0;
int count_copy=0;
int make_note=0;
char* do_note_list;

int readint(){
    char buf[8];
    return atoi(fgets(buf,8,stdin));
}

void create_name(){
    unsigned size = 0,now=0;
    while(name_list[now].addr_name != NULL){
        now++;
    }

    if (0 <= count_name && count_name<=14){
        printf("Input size: ");
        size = readint();
        if (0 < size && size <= 0x500){
            name_list[now].addr_name = calloc(1,size);
            name_list[now].size = size;
            count_name++;
        }else{
            printf("error\n");
            return;
        }
    }else{
        printf("Full\n");
        return;
    }

}

void delete_name(){
    unsigned idx;
    printf("Input index: ");
    idx = readint();
    if ((0<= idx && idx <= 8) && name_list[idx].addr_name != 0 ){
        free(name_list[idx].addr_name);
        name_list[idx].addr_name = NULL;
        name_list[idx].size= 0;
        count_name--;
    }else{
        printf("error\n");
        return;
    }
}

void view_name(){
    unsigned idx;
    printf("Input index: ");
    idx = readint();
    if ((0<= idx && idx <= 8) && name_list[idx].addr_name != 0 ){
        write(1, name_list[idx].addr_name, name_list[idx].size);
    }else{
        printf("error\n");
        return;
    }
}

void edit_name(){
    unsigned idx;
    printf("Input index: ");
    idx = readint();
    if ((0<= idx && idx <= 8) && name_list[idx].addr_name != 0 ){
        printf("Your name: ");
        read(0, name_list[idx].addr_name, name_list[idx].size);
    }else{
        printf("error\n");
        return;
    }
}

void copy_name(){
    unsigned int src,dst,size;

    printf("Source index: ");
    src = readint();
    printf("Destination index: ");
    dst = readint();
    if (count_copy == 0){
        if ((0<= src && src <= 8) && name_list[src].addr_name != 0 ){
            if ((0<= dst && dst <= 8) && name_list[dst].addr_name != 0 ){
                size=strlen(name_list[src].addr_name);
                strncpy(name_list[dst].addr_name,name_list[src].addr_name,size);
                count_copy++;
            }
        }else{
            printf("error\n");  
        }
    }else{
        printf("error\n");
    }
    return;
}


void add_note(){
    if( count_note == 0 || count_note == 1){
        note_list[count_note].addr_note = malloc(0x100);
        note_list[count_note].size = 0x100;
        printf("Your note: ");
        read(0, note_list[count_note].addr_note, note_list[count_note].size);
        count_note++;
    }else{
        printf("error\n");
    }
}

void init(){
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(120);
}

int menu(){
    printf("Blacklist Name\n");
    printf("Menu:\n");
    printf("1. Add Name.\n");
    printf("2. Delete Name.\n");
    printf("3. View Name.\n");
    printf("4. Edit Name.\n");
    printf("5. Copy Name.\n");
    printf("6. Write Note.\n");
    printf("> ");
    return readint();
}

int main(){
    init();
    // setup_seccomp();
    while(1){
        switch(menu()){
        case 1:
            create_name();
            break;
        case 2:
            delete_name();
            break;
        case 3:
            view_name();
            break;
        case 4:
            edit_name();
            break;
        case 5:
            copy_name();
            break;
        case 6:
            add_note();
            break;
        default:
            exit(0);
        }
    }
    return 0;
}
