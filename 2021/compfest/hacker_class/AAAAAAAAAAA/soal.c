#include<stdio.h>
#include<stdlib.h>

int main(int argc, char const *argv[])
{
	setvbuf(stdout, NULL, _IONBF, 0);
	
	char buf1[14] = "RegularBuffer\0";
	char buf2[14] = "RegularBuffer\0";
	printf("Contents of buffer:\n");
	printf("buf1: %s\n", buf1);
	printf("buf2: %s\n", buf2);

	gets(buf1);

	printf("Contents of buffer:\n");
	printf("buf1: %s\n", buf1);
	printf("buf2: %s\n", buf2);

	if(memcmp(buf2, "BufferOverflow", sizeof(buf2)) == 0)	{
		puts("Gratz");
		system("cat flag.txt");
	}
	return 0;
}