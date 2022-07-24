void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  dword_404160 = 0;
  puts("Welcome to paper title !");
  puts("Here, you can write the title of the paper that you will remember for the rest of your life");
  while ( 1 )
  {
    switch ( (unsigned int)sub_4012BE() )
    {
      case 1u:
        sub_401347();
        break;
      case 2u:
        sub_4013A8();
        break;
      case 3u:
        sub_40157D();
        break;
      case 4u:
        sub_401601();
        break;
      case 5u:
        sub_401685();
        break;
      case 6u:
        puts("[+] Exiting ...");
        exit(0);
      default:
        puts("[!] Error : wrong choice !");
        break;
    }
  }
}

__int64 sub_401347()
{
  __int64 result; // rax
  unsigned int i; // [rsp+Ch] [rbp-4h]

  for ( i = 0; ; ++i )
  {
    result = (unsigned int)dword_404160;
    if ( i >= dword_404160 )
      break;
    printf("[%d] - %s", i + 1, *(const char **)(qword_4040C0[i] + 16LL));
  }
  return result;
}

void sub_4013A8()
{
  unsigned int *ptr; // [rsp+0h] [rbp-10h]
  int v1; // [rsp+8h] [rbp-8h]
  int v2; // [rsp+Ch] [rbp-4h]

  if ( (unsigned int)dword_404160 <= 0x13 )
  {
    ptr = (unsigned int *)malloc(0x30uLL);
    v2 = sub_40123F("Title size");
    v1 = sub_40123F("Content size");
    if ( v2 > 0 && v1 > 0 )
    {
      ptr[6] = v2 + 2;
      ptr[2] = v1 + 2;
      *(_QWORD *)ptr = malloc(ptr[2]);
      *((_QWORD *)ptr + 2) = malloc(ptr[6]);
      *((_QWORD *)ptr + 5) = sub_4011F3;
      *((_QWORD *)ptr + 4) = sub_401196;
      printf("Title > ");
      fgets(*((char **)ptr + 2), ptr[6], stdin);
      *(_BYTE *)(*((_QWORD *)ptr + 2) + ptr[6] - 2) = 10;
      printf("Content > ");
      fgets(*(char **)ptr, ptr[2], stdin);
      *(_BYTE *)(*(_QWORD *)ptr + ptr[2] - 2) = 10;
      qword_4040C0[dword_404160++] = ptr;
    }
    else
    {
      puts("[!] Error : bad size !");
      free(ptr);
    }
  }
  else
  {
    puts("[!] Error : too much papers !");
  }
}

int sub_40157D()
{
  int v1; // [rsp+Ch] [rbp-4h]

  v1 = sub_40123F("paper number");
  if ( v1 > 0 && dword_404160 + 1 > (unsigned int)v1 )
    return (*(__int64 (__fastcall **)(_QWORD))(qword_4040C0[v1 - 1] + 40LL))(qword_4040C0[v1 - 1]);
  else
    return puts("[!] Error : wrong paper number !");
}

int sub_401601()
{
  int v1; // [rsp+Ch] [rbp-4h]

  v1 = sub_40123F("paper number");
  if ( v1 > 0 && dword_404160 + 1 > (unsigned int)v1 )
    return (*(__int64 (__fastcall **)(_QWORD))(qword_4040C0[v1 - 1] + 32LL))(qword_4040C0[v1 - 1]);
  else
    return puts("[!] Error : wrong paper number !");
}

int sub_401685()
{
  int v1; // [rsp+Ch] [rbp-4h]

  v1 = sub_40123F("paper number");
  if ( v1 <= 0 || dword_404160 + 1 <= (unsigned int)v1 )
    return puts("[!] Error : wrong paper number !");
  free((void *)qword_4040C0[v1 - 1]);
  return --dword_404160;
}

_BYTE *__fastcall sub_401196(__int64 a1)
{
  _BYTE *result; // rax

  printf("Content > ");
  fgets(*(char **)a1, *(_DWORD *)(a1 + 8), stdin);
  result = (_BYTE *)(*(_QWORD *)a1 + (unsigned int)(*(_DWORD *)(a1 + 8) - 2));
  *result = 10;
  return result;
}

int __fastcall sub_4011F3(const char **a1)
{
  printf("[+] %s", a1[2]);
  return printf("[>] %s", *a1);
}