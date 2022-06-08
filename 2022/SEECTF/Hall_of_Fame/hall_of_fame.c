int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  char *v4; // rax
  __int64 v5; // rcx
  __int64 v6; // rcx
  __int64 v7; // rcx
  __int64 v8; // rcx
  __int64 v9; // rcx
  __int64 v10; // rcx
  int counter; // [rsp+8h] [rbp-E8h]
  char *pty; // [rsp+10h] [rbp-E0h] BYREF
  void *heap_pointer; // [rsp+18h] [rbp-D8h]
  unsigned __int64 size; // [rsp+20h] [rbp-D0h]
  char *ptr; // [rsp+28h] [rbp-C8h]
  char *chunk; // [rsp+30h] [rbp-C0h]
  char option[3]; // [rsp+3Dh] [rbp-B3h] BYREF
  char score[64]; // [rsp+40h] [rbp-B0h] BYREF
  char word[100]; // [rsp+80h] [rbp-70h] BYREF
  unsigned __int64 v21; // [rsp+E8h] [rbp-8h]

  v21 = __readfsqword(0x28u);
  counter = 0;
  heap_pointer = sbrk(0LL);
  setup_IO();
  while ( 1 )
  {
    while ( 1 )
    {
      do
      {
        print_statements(counter);
        printf("Choose> ");
        fflush(stdout);
      }
      while ( !fgets(option, 3, stdin) );
      fflush(stdin);
      option[strcspn(option, "\n")] = 0;
      v3 = atoi(option);
      if ( v3 != 2 )
        break;
      printf("\nThe position of latest addition is at %p\n", heap_pointer);
      printf("The position of PUTS is at %p\n", &puts);
    }
    if ( v3 == 3 )
      break;
    if ( v3 == 1 )
    {
      printf("\nHow many points did this person score? > ");
      fflush(stdout);
      if ( fgets(score, 64, stdin) )
      {
        fflush(stdin);
        score[strcspn(score, "\n")] = 0;
        size = strtol(score, &pty, 10);
        ptr = (char *)malloc(size);
        chunk = ptr;
        printf("\nWho is this Hall of Famer > ");
        fflush(stdout);
        fgets(word, 100, stdin);
        fflush(stdin);
        v4 = chunk;
        v5 = *(_QWORD *)&word[8];
        *(_QWORD *)chunk = *(_QWORD *)word;
        *((_QWORD *)v4 + 1) = v5;
        v6 = *(_QWORD *)&word[24];
        *((_QWORD *)v4 + 2) = *(_QWORD *)&word[16];
        *((_QWORD *)v4 + 3) = v6;
        v7 = *(_QWORD *)&word[40];
        *((_QWORD *)v4 + 4) = *(_QWORD *)&word[32];
        *((_QWORD *)v4 + 5) = v7;
        v8 = *(_QWORD *)&word[56];
        *((_QWORD *)v4 + 6) = *(_QWORD *)&word[48];
        *((_QWORD *)v4 + 7) = v8;
        v9 = *(_QWORD *)&word[72];
        *((_QWORD *)v4 + 8) = *(_QWORD *)&word[64];
        *((_QWORD *)v4 + 9) = v9;
        v10 = *(_QWORD *)&word[88];
        *((_QWORD *)v4 + 10) = *(_QWORD *)&word[80];
        *((_QWORD *)v4 + 11) = v10;
        *((_DWORD *)v4 + 24) = *(_DWORD *)&word[96];
        heap_pointer = ptr;
        ++counter;
      }
    }
    else
    {
      puts("No choice Given!");
    }
  }
  puts("Exiting software...");
  return 0;
}