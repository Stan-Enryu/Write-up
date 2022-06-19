all:
	gcc -g -Wl,-z,relro,-z,now -fstack-protector-all chall.c -o chall -lseccomp
	patchelf --set-interpreter ./ld-2.31.so ./chall
	patchelf --replace-needed libc.so.6 ./libc.so.6 ./chall
