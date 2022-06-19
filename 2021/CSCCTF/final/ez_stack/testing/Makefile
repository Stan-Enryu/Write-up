all:
	gcc -g -Wl,-z,relro,-z,now -no-pie chall.c -o chall
	patchelf --set-interpreter ./ld-2.31.so ./chall
	patchelf --replace-needed libc.so.6 ./libc.so.6 ./chall