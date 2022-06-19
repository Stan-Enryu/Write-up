//gcc -g -Wl,-z,relro,-z,now -fstack-protector-all -no-pie soal.c -o soal
//patchelf --set-interpreter ld.so ./soal
// glibc 2.29
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<unistd.h>

char *Paragraf[10];
long int Banyak_Paragraf=0;
long int Index_Paragraf=0;

void init(){
	setvbuf(stdin, 0LL, 2, 0LL);
  	setvbuf(stdout, 0LL, 2, 0LL);
}
void menu(){
	printf("1. Tulis Cerpen\n");
	printf("2. Tulis ulang\n");
	printf("3. Kirim Cerpen\n");
}
void Tulis_Paragraf(){
	int Panjang_Tulisan;
	char *tulisan;
	
	if ( Index_Paragraf == Banyak_Paragraf ){
	    printf("Sudah sampai batas\n");
	} else {
	    printf("Panjang : ");
	    scanf("%i",&Panjang_Tulisan);
    	getchar();
    	printf("Tulis diKolom %i :\n",Index_Paragraf+1);
	    if ( Panjang_Tulisan >= 0 && Panjang_Tulisan <= 200 ){
	      tulisan = malloc(Panjang_Tulisan + 1);
	      if ( !tulisan ){
	        exit(1);
	      }
	      fgets(tulisan,Panjang_Tulisan,stdin);
	      
	      Paragraf[Index_Paragraf] = tulisan;
	      Index_Paragraf++;
	      printf("Nice\n");
	    }else{
	      printf("Terlalu Panjang");
	    }
  	}
}

void Kirim_Cerpen(){
	Index_Paragraf = Index_Paragraf - Banyak_Paragraf;
	for(int i=0;i<10;i++){
		Paragraf[i]=0;
	}

}
int main(){
	char *nama;
	init();
	printf("Menulis Cerpen\n");
	while(1){
		char Check[10];
		printf("Masukan Nama : ");
		nama = malloc(32);
		read(0, nama, 31);
		printf("Banyak paragraf : ");
		scanf("%ld",&Banyak_Paragraf);
		getchar();
		if(Banyak_Paragraf <= 10){
			while(1){
				int pilih;
				menu();
				printf("Input: ");
				scanf("%d",&pilih);
				getchar();
				if(pilih>=1&&pilih<=3){
					if(pilih==1){
						Tulis_Paragraf();
					}else if(pilih==2){
						Index_Paragraf = Index_Paragraf - Index_Paragraf;
						printf("Cerpen akan dimulai dari kolom ke 1");
					}else if(pilih==3){
						Kirim_Cerpen();
						printf("Selamat %sberhasil mengirimkan Cerpennya\n",nama);
						break;
					}
				}else{
					printf("Input invalid\n");
				}
			}
		}else{
			printf("Cerpen gak sebanyak itu\n");
			exit(1);
		}
		printf("Apakah Kamu mau menulis cerpen lagi (yes/no)? ");
		fgets(Check,10,stdin);
		if(strncmp(Check,"yes",3)!=0){
			printf("Bye\n");
			exit(1);
		}
	}
}