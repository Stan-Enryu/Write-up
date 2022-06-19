#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <fcntl.h>
#include <seccomp.h>

const char sc[] = "H\x89\xfcH1\xc0H1\xdbH1\xc9H1\xd2H1\xffH1\xf6H1\xedM1\xc0M1\xc9M1\xd2M1\xdbM1\xe4M1\xedM1\xf6M1\xff";
void *rwx, *rw;

void setup_seccomp()
{
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
	seccomp_rule_add(
		ctx,
		SCMP_ACT_ALLOW,
		SCMP_SYS(exit),
		0
	);
	seccomp_rule_add(
		ctx,
		SCMP_ACT_ALLOW,
		SCMP_SYS(exit_group),
		0
	);
	seccomp_rule_add(
		ctx,
		SCMP_ACT_ALLOW,
		SCMP_SYS(getdents64),
		0
	);
	seccomp_rule_add(
		ctx,
		SCMP_ACT_ALLOW,
		SCMP_SYS(openat),
		0
	);
	seccomp_rule_add(
		ctx,
		SCMP_ACT_ALLOW,
		SCMP_SYS(read),
		0
	);
	seccomp_rule_add(
		ctx,
		SCMP_ACT_ALLOW,
		SCMP_SYS(write),
		0
	);
	if(seccomp_load(ctx) < 0) exit(-1);
}

void get_random_address()
{
	unsigned long long a1,a2;
	int fd = open("/dev/urandom",O_RDONLY);
	if(fd < 0) exit(-1);
	read(fd,&a1,8);
	a1 &= 0xfffffff000;
	rwx = mmap((void *)a1,0x1000,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
	read(fd,&a2,8);
	a2 &= 0xfffffff000;
	rw = mmap((void *)a2,0x1000,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
	if((unsigned long long)rwx != a1 || (unsigned long long)rw != a2) exit(-1);
}

void initialize()
{
	setvbuf(stdout,0,2,0);
	get_random_address();
	alarm(30);
}

int main()
{
	initialize();
	puts("babysc");
	puts("======");
	printf("Shellcode: ");
	size_t n = read(0,rwx+48,0x100);
	memcpy(rwx,sc,48);
	mprotect(rwx,0x1000,PROT_READ|PROT_EXEC);
	setup_seccomp();
	((void(*)(void *))rwx)(rw+0x500);
	return 0;
}