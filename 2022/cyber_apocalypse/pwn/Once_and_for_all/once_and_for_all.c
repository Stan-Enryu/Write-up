int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+18h] [rbp-8h] BYREF
  int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; i <= 49; ++i )
  {
    puts(s);
    printf(&byte_1310);
    __isoc99_scanf(&unk_13C8, &v4);
    puts(s);
    switch ( v4 )
    {
      case 1:
        small_alloc(s);
        break;
      case 2:
        fix(s);
        break;
      case 3:
        examine(s);
        break;
      case 4:
        savebig(s);
        break;
      case 5:
        exit(0);
      default:
        puts("[-] Invalid choice!");
        break;
    }
  }
  return 0;
}

int small_alloc()
{
  unsigned __int64 v1; // rbx
  size_t nmemb; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v3[3]; // [rsp+8h] [rbp-18h] BYREF

  if ( allocated == 15 )
    return puts("Nothing more!");
  ++allocated;
  printf("Choose an index: ");
  __isoc99_scanf("%lu", v3); // INPUT
  if ( *((_QWORD *)&weapons + 2 * v3[0]) || *((_QWORD *)&unk_202088 + 2 * v3[0]) || v3[0] > 0xE )
    return puts("[-] Invalid!");
  printf("\nHow much space do you need for it: ");
  __isoc99_scanf("%lu", &nmemb); // INPUT
  if ( nmemb <= 0x1F || nmemb > 0x38 )
    return puts("[-] Your inventory cannot provide this type of space!");
  *((_QWORD *)&weapons + 2 * v3[0]) = nmemb;
  v1 = v3[0];
  *((_QWORD *)&unk_202088 + 2 * v1) = calloc(nmemb, 1uLL);

  if ( !*((_QWORD *)&unk_202088 + 2 * v3[0]) )
  {
    puts("[-] Something didn't work out...");
    exit(-1);
  }
  puts("Input your weapon's details: ");
  return read(0, *((void **)&unk_202088 + 2 * v3[0]), nmemb + 1); //INPUT
}

int fix()
{
  int result; // eax
  unsigned __int64 v1; // rbx
  unsigned __int64 v2; // [rsp+8h] [rbp-28h] BYREF
  size_t nmemb; // [rsp+10h] [rbp-20h] BYREF
  __int64 v4[3]; // [rsp+18h] [rbp-18h] BYREF

  printf("Choose an index: ");
  __isoc99_scanf("%lu", &v2);
  if ( !*((_QWORD *)&weapons + 2 * v2) || !*((_QWORD *)&unk_202088 + 2 * v2) || v2 > 0xE )
    return puts("[-] Invalid!");
  puts("Ok, let's get you some new parts for this one... seems like it's broken");
  free(*((void **)&unk_202088 + 2 * v2));
  printf("\nHow much space do you need for this repair: ");
  __isoc99_scanf("%lu", &nmemb);
  if ( nmemb <= 0x1F || nmemb > 0x38 )
    return puts("[-] Your inventory cannot provide this type of space.");
  *((_QWORD *)&weapons + 2 * v2) = nmemb;
  v1 = v2;
  *((_QWORD *)&unk_202088 + 2 * v1) = calloc(nmemb, 1uLL);
  if ( !*((_QWORD *)&unk_202088 + 2 * v2) )
  {
    puts("Something didn't work out...");
    exit(-1);
  }
  puts("Input your weapon's details: ");
  read(0, *((void **)&unk_202088 + 2 * v2), nmemb);
  printf("What would you like to do now?\n1. Verify weapon\n2. Continue\n>> ");
  __isoc99_scanf("%lu", v4);
  result = v4[0];
  if ( v4[0] == 1 )
  {
    if ( verified )
    {
      return puts(&byte_1648);
    }
    else
    {
      result = puts(*((const char **)&unk_202088 + 2 * v2));
      verified = 1;
    }
  }
  return result;
}

int examine()
{
  unsigned __int64 v1; // [rsp+8h] [rbp-8h] BYREF

  if ( examined )
    return puts(&byte_14D0);
  examined = 1;
  printf("Choose an index: ");
  __isoc99_scanf("%lu", &v1);
  if ( *((_QWORD *)&weapons + 2 * v1) && *((_QWORD *)&unk_202088 + 2 * v1) && v1 <= 0xE )
    return puts(*((const char **)&unk_202088 + 2 * v1));
  else
    return puts("[-] Invalid!");
}


int savebig()
{
  void *v0; // rax
  size_t size; // [rsp+8h] [rbp-8h] BYREF

  if ( chungus_weapon || qword_202068 )
  {
    LODWORD(v0) = puts(&byte_16E8);
  }
  else
  {
    printf("How much space do you need for this massive weapon: ");
    __isoc99_scanf("%lu", &size);
    if ( (unsigned __int16)size > 0x5AFu && (unsigned __int16)size <= 0xF5C0u )
    {
      puts("Adding to your inventory..");
      chungus_weapon = size;
      v0 = malloc(size);
      qword_202068 = (__int64)v0;
    }
    else
    {
      LODWORD(v0) = puts("[-] This is not possible..");
    }
  }
  return (int)v0;
}