#include <stdio.h>
#include <string.h>
#include <stdlib.h>


char format_specifier[0x10];


int main(){
	strcpy(format_specifier,"%256s");
	char data[256];
	char * filter[11];
	filter[0]="c";
	filter[1]="s";
	filter[2]="i";
	filter[3]="u";
	filter[4]="f";
	filter[5]="d";
	filter[6]="o";
	filter[7]="x";
	filter[8]="p";
	filter[9]="e";
	filter[10]="E";
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	puts("Hey there, this is a classic echo server :) I'll repeat after you. \\o/");
	int j;
	for(j=0; j<2;j++){
		printf("\ninput>");
		scanf(format_specifier,data);
		// filtering
		int i;
		int no=0;
		for( i=0; i<11;i++){
			if (strstr(data, filter[i]) != NULL) {
				no=1;
			}
		}
		if (!no){
			printf(data);
		}
		
	}

	return 0;
}

//gcc -o main task.c -fno-stack-protector -no-pie