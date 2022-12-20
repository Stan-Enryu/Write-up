#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void give_shell()
{
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	system("/bin/sh -i");
}

int main(int argc, char **argv)
{
	char buffer[256];
	int pos = 0;

	printf("Selamat datang ke buffer management:\n\n");
	while(1)
	{
		int len;
		printf("Mau berapa bytes? "); fflush(stdout);
		scanf("%u", &len);
		fgets(buffer, 2, stdin);

		if (len == 0) break;

		printf("Masukkan data anda: "); fflush(stdout);
		if (len < 256 - pos)
		{
			fgets(&buffer[pos], len, stdin);
			pos = pos + len;
		}
		else
		{
			fgets(&buffer[pos], 256 - pos, stdin);
			len = len - (256 - pos);
			pos = 0;

			fgets(&buffer[0], len, stdin);
			pos = pos + len;
		}

		printf("\n");
	}

	return 0;
}
