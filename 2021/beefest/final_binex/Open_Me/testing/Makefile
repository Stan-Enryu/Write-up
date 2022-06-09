all:
	gcc -no-pie -g -Wl,-z,relro,-z,now chall.c -z execstack -fno-stack-protector -o chall -lseccomp