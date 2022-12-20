#include <stdio.h>
#include <unistd.h>
#include <string.h>

void init(){
    setvbuf(stdout, NULL, _IOLBF, 0);
}

void ask(){
	char *words = "Untuk apa hidup ini?";
	puts(words);
}

void answr(){
	char buffer[16] = {0};
	read(0, buffer, 0x80);
}

int main(){
    init();
    ask();
    answr();
	return 0;
}
