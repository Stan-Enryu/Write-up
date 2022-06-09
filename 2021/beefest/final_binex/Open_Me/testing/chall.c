//gcc -g -Wl,-z,relro,-z,now chall.c -fstack-protector-all -o chall -lseccomp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <seccomp.h>

void setup_seccomp(){
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(open),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(openat),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(read),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(write),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit_group),0);
    if(seccomp_load(ctx) < 0) exit(-1);
}

void init(){
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(120);
}

int main(){
    init();
    setup_seccomp();
    char buff[8];
    printf("Your reward : %p\n",&buff);
    fgets(buff,112,stdin);
}
