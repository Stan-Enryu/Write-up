__int64 __fastcall sub_401389(int a1, int a2)
{
  unsigned int v2; // eax

  v2 = time(0LL);
  srand(v2);
  return (unsigned int)(rand() % a1 + a2);
}

__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  char v3; // bl
  int v5; // [rsp+1Ch] [rbp-34h] BYREF
  unsigned int v6; // [rsp+20h] [rbp-30h] BYREF
  unsigned int v7; // [rsp+24h] [rbp-2Ch] BYREF
  int v8; // [rsp+28h] [rbp-28h] BYREF
  int v9; // [rsp+2Ch] [rbp-24h]
  char v10[8]; // [rsp+30h] [rbp-20h]
  unsigned __int64 v11; // [rsp+38h] [rbp-18h]

  v11 = __readfsqword(0x28u);
  sub_401276(a1, a2, a3);
  sub_4012DB();
  v9 = 0;
  while ( 1 )
  {
    puts("1) Try scrambling");
    puts("2) Quit");
    printf("> ");
    __isoc99_scanf("%d", &v5);
    if ( v5 != 1 )
      break;
    if ( v9 > 7 )
    {
      puts("Not allowed!");
    }
    else
    {
      puts("arg1 = ");
      printf("> ");
      __isoc99_scanf("%d", &v6);
      puts("arg2 = ");
      printf("> ");
      __isoc99_scanf("%d", &v7);
      puts("arg3 = ");
      printf("> ");
      __isoc99_scanf("%d", &v8);
      v3 = v8;
      v10[(int)sub_401389(v6, v7)] = v3;
      ++v9;
    }
  }
  puts("Good bye!");
  return 0LL;
}