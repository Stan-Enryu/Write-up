#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
//gcc -no-pie soal.c -o soal
extern char __bss_start;
extern char _end;
extern char etext;
extern char __int64;

void init(){
  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
}

void need_more(){
  __asm__( "pop %rdx;"
            "ret;"
            "syscall;"
            "mov $1342,%esp;"
            "ret;"
    );
}

unsigned long max(unsigned long a,unsigned long b){
  if (a >= b){
    return a;
  }else{
    return b;
  }
}
long long now,temp,i=0;
int main(){
  init();
  // long long now,temp,i=0;
  char buf[64];
   
  // memset(buf, 0, sizeof(buf));
  printf("Ara - Ara kurumi the best\nWhat do you think? ");
  temp=read(0, buf, 1000);
  // printf("%ld\n",temp);
  while ( temp / 8 != i ){
    now = *(long long int*)&buf[8 * i];
    // printf("%p\n",now);
    if ( 255 < now && now < (long long int)&need_more 
      || (long long int)&etext < now && now < (long long int)&__bss_start 
      || (long long int)&_end < now ){
      printf("GG:)\n");
      exit(1);
    }
    i++;
  }
  return 0;
}