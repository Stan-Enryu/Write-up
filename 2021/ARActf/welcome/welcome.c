#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

void ignore_me() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}


void win() {
    printf("┌───────────────────────┐\n");
    printf("│        Horrayyy       │\n");
    printf("└───────────────────────┘\n");
    system("cat flag");
}

void welcome() {
    printf(" addr of welcome(): %p\n", welcome);
    printf("┌───────────────────────┐\n");
    printf("│  Welcome to ARA 2021  │\n");
    printf("└───────────────────────┘\n");
}

void vuln() {
    char buff[0xff];
    printf(" Input keys to generate flag:\n");
    gets(buff);
    if(strcmp(buff, "ARA2021") == 0) {
        printf(" Where is The flag?\n");
    } else {
        _exit(0);
    }
}


void main(int argc, char* argv[]) {
    ignore_me();
    welcome();
    vuln();
}


