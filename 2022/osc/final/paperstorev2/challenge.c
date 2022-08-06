int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  char buf[2]; // [rsp+Ah] [rbp-6h] BYREF
  int v4; // [rsp+Ch] [rbp-4h]

  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  while ( 1 )
  {
    while ( 1 )
    {
      while ( 1 )
      {
        menu();
        if ( read(0, buf, 2uLL) )
          break;
        perror("Error read option\r\n");
      }
      v4 = atol(buf);
      if ( v4 != 3 )
        break;
      view_papers();
    }
    if ( v4 > 3 )
    {
LABEL_12:
      puts("Invalid option");
    }
    else if ( v4 == 1 )
    {
      add_paper();
    }
    else
    {
      if ( v4 != 2 )
        goto LABEL_12;
      remove_paper();
    }
  }
}

unsigned int add_paper()
{
  const char *v1; // rbx
  const char *v2; // rbx
  unsigned __int64 size; // [rsp+8h] [rbp-28h]
  void *v4; // [rsp+10h] [rbp-20h]
  int i; // [rsp+1Ch] [rbp-14h]

  if ( num_papers == 16 )
    return puts("Cart limit reached!");
  v4 = malloc(0x38uLL);
  printf("Paper name length: ");
  size = readint();
  if ( size > 0xFF )
    return puts("Too bigger!");

  printf("Paper name: ");
  *((_QWORD *)v4 + 1) = malloc(size);
  read(0, *((void **)v4 + 1), size);
  v1 = (const char *)*((_QWORD *)v4 + 1);
  if ( v1[strlen(v1) - 1] == 10 )
  {
    v2 = (const char *)*((_QWORD *)v4 + 1);
    v2[strlen(v2) - 1] = 0;
  }
  printf("Paper price: ");
  *((_QWORD *)v4 + 2) = readint();
  for ( i = 0; *((_QWORD *)&papers + i); ++i )
    ;
  *((_QWORD *)&papers + i) = v4;
  **((_QWORD **)&papers + i) = i;
  ++num_papers;
  return (unsigned int)strcpy((char *)(*((_QWORD *)&papers + i) + 24LL), 'Copyright Paper Store V2');
}

int remove_paper()
{
  unsigned __int64 v1; // [rsp+8h] [rbp-8h]

  printf("Paper index: ");
  v1 = readint();
  if ( v1 >= (unsigned int)num_papers )
    return puts("Invalid index");
  free(*(void **)(*((_QWORD *)&papers + v1) + 8LL));
  free(*((void **)&papers + v1));
  return --num_papers;
}

int view_papers()
{
  __int64 v1; // [rsp+0h] [rbp-10h]
  int i; // [rsp+Ch] [rbp-4h]

  puts("{");
  puts("\t\"Papers\" : [");
  for ( i = 0; i <= 15; ++i )
  {
    if ( *((_QWORD *)&papers + i) )
    {
      v1 = **((_QWORD **)&papers + i);
      puts("\t\t{");
      printf("\t\t\t\"index\": %ld,\n", v1);
      printf("\t\t\t\"name\": \"%s\",\n", *(const char **)(*((_QWORD *)&papers + i) + 8LL));
      printf("\t\t\t\"price\": %ld,\n", *(_QWORD *)(*((_QWORD *)&papers + i) + 16LL));
      printf("\t\t\t\"rights\": \"");
      printf((const char *)(*((_QWORD *)&papers + i) + 24LL));
      puts("\"");
      if ( *((_QWORD *)&papers + i + 1) )
        puts("\t\t},");
      else
        puts("\t\t}");
    }
  }
  puts("\t]");
  return puts("}");
}

int menu()
{
  puts("Paper Store V.2");
  puts("1 Add paper to cart");
  puts("2 Remove from cart");
  puts("3 View cart");
  puts("4 Checkout!");
  return printf("> ");
}