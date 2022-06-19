all:
	gcc -g -Wl,-z,relro,-z,now chall.c -fstack-protector-all -o chall
	patchelf --set-interpreter ./ld-2.27.so ./chall
	patchelf --replace-needed libc.so.6 ./libc-2.27.so ./chall
