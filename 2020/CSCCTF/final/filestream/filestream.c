#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

#ifdef DEBUG
	const char *flagpath = "./flag.txt";
#endif

#ifndef DEBUG
	const char *flagpath = "/home/filestream/flag.txt";
#endif

struct target
{
	char flag[64];
	char buf[256];
	FILE *f;
};

struct target t;

void setup_flag()
{
	int fd = open(flagpath,O_RDONLY);
	read(fd,&t.flag,64);
	close(fd);
}

void initialization()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setup_flag();
	alarm(30);
}

char *setup_file()
{
	char *fname,randoms[8],c;
	fname = calloc(64,sizeof(char));
	int fd = open("/dev/urandom",O_RDONLY);
	for(int i=0;i<8;)
	{
		read(fd,&c,1);
		if((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9'))
		{
			randoms[i++] = c;
		}
	}
	sprintf(fname,"/tmp/filestream-%s",randoms);
	close(open(fname,O_CREAT|O_WRONLY,S_IRUSR|S_IWUSR));
	return fname;
}

int main()
{
	initialization();
	printf("Filestream\n==========\n\n");
	printf("Here's your gift: %p\n",&printf);
	char *s = setup_file();
	t.f = fopen(s,"r+");
	printf("Your text: ");
	read(0,&t.buf,512);
	fwrite(t.buf,256,sizeof(char),t.f);
	fclose(t.f);
	unlink(s);
	exit(0);
}