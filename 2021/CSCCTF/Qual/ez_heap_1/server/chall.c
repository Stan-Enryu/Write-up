//gcc -g -Wl,-z,relro,-z,now chall.c -fstack-protector-all -o chall
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

struct name {
    char* addr_name;
    size_t size;
};

struct name name_list[8];
int count_name=0;

int readint(){
    char buf[8];
    return atoi(fgets(buf,8,stdin));
}

void create_name(){
    unsigned size = 0,now=0;
    while(name_list[now].addr_name != NULL){
        now++;
    }

    if (0 <= count_name && count_name<=8){
        printf("Input size: ");
        size = readint();
        if (0 < size && size <= 0x400){
            name_list[now].addr_name = calloc(1, size);
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

void edit_name(){
    unsigned idx;
    printf("Input index: ");
    idx = readint();
    if ((0<= idx && idx <= 8) && name_list[idx].addr_name != 0 ){
        printf("Your name: ");
        read(0, name_list[idx].addr_name, name_list[idx].size-1);
    }else{
        printf("error\n");
        return;
    }
}

void copy_name(){
    unsigned src,dst;

    printf("Source index: ");
    src = readint();
    printf("Destination index: ");
    dst = readint();

    if ((0<= src && src <= 8) && name_list[src].addr_name != 0 ){
        if ((0<= dst && dst <= 8) && name_list[dst].addr_name != 0 ){
            strcpy(name_list[dst].addr_name,name_list[src].addr_name);
        }
    }else{
        printf("error\n");
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
    printf("> ");
    return readint();
}

int main(){
    init();
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
        default:
            exit(0);
        }
    }
    return 0;
}
