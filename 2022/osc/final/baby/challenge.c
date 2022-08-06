int __cdecl main(int argc, const char **argv, const char **envp)
{
  size_t v4; // rax
  char v5[2]; // [rsp+Dh] [rbp-63h] BYREF
  char v6[81]; // [rsp+Fh] [rbp-61h] BYREF
  char *s; // [rsp+60h] [rbp-10h]
  unsigned __int8 i; // [rsp+6Fh] [rbp-1h]

  setbuf(stdin, 0LL);
  setbuf(_bss_start, 0LL);
  v6[0] = 0;
  puts("make fortune chests?\r");
  __isoc99_scanf("%2s", v5);
  if ( v5[0] == 107 || v5[0] == 75 )
  {
    printf("name: ");
    s = (char *)malloc(0x64uLL);
    strcpy(s, "fortune chests : ");
    __isoc99_scanf("%50s", s + 14);
    v4 = strlen(s);
    strcpy(&s[v4], " created!\r\n");
    puts("How many chips do you have?\r");
    __isoc99_scanf("%hhu", v6);
    if ( v6[0] > 20 )
    {
      perror("Lots of chips don't support :/\r\n");
      exit(1);
    }
    for ( i = 0; i < (unsigned int)v6[0]; ++i )
      __isoc99_scanf("%d", &v6[4 * i + 1]);
    printf(s);
    free(s);
    return 0;
  }
  else
  {
    puts("Bye!\r");
    return 0;
  }
}