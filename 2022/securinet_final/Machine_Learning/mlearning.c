__int64 sub_145D()
{
  char buf[8]; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  read(0, buf, 7uLL);
  return (unsigned int)atoi(buf);
}

ssize_t sub_14BB()
{
  puts("1- New Record");
  puts("2- Swap two Records");
  puts("3- Delete Record");
  puts("4- Show Records");
  puts("5- leave");
  return write(1, &off_207E, 2uLL);
}

__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  int v4; // [rsp+Ch] [rbp-14h]
  char buf[8]; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v6; // [rsp+18h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  sub_1309();
  puts("Identification Process:");
  read(0, buf, 7uLL);
  qword_4100 = (__int64)buf;
  printf("Welcome #%s:Please help us improve our Machine Learning model, Thanks!\n", buf);
  while ( v4 != 5 )
  {
    sub_14BB();
    v4 = sub_145D();
    if ( v4 == 4 )
    {
      sub_16F2();
    }
    else if ( v4 <= 4 )
    {
      if ( v4 == 3 )
      {
        sub_1659();
      }
      else if ( v4 <= 3 )
      {
        if ( v4 == 1 )
        {
          sub_151D();
        }
        else if ( v4 == 2 )
        {
          sub_177C();
        }
      }
    }
  }
  return 0LL;
}

int sub_151D()
{
  int result; // eax
  int i; // [rsp+8h] [rbp-8h]
  int v2; // [rsp+Ch] [rbp-4h]

  if ( dword_4170 > 19 )
    return puts("The model memory is not that large :/");
  puts("short name or long name?(0,1)");
  result = sub_145D();
  v2 = result;
  for ( i = 0; i <= 19; ++i )
  {
    result = dword_4120[i];
    if ( !result )
    {
      *((_QWORD *)&unk_4060 + i) = malloc(24 * v2 + 304);
      dword_4120[i] = 1;
      puts("Record description:");
      read(0, *((void **)&unk_4060 + i), (unsigned int)(24 * v2 + 304));
      printf("New record at index %d\n", (unsigned int)i);
      return ++dword_4170;
    }
  }
  return result;
}


int sub_177C()
{
  signed int v1; // [rsp+8h] [rbp-7E8h]
  signed int v2; // [rsp+Ch] [rbp-7E4h]
  char dest[2008]; // [rsp+10h] [rbp-7E0h] BYREF
  unsigned __int64 v4; // [rsp+7E8h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  puts("Give 2 indexes to swap their order:");
  v1 = sub_145D();
  v2 = sub_145D();
  if ( (unsigned int)v1 <= 0x13 && (unsigned int)v2 <= 0x13 )
  {
    strcpy(dest, *((const char **)&unk_4060 + v1));
    strcpy(*((char **)&unk_4060 + v1), *((const char **)&unk_4060 + v2));
    strcpy(*((char **)&unk_4060 + v2), dest);
  }
  return puts("Done!");
}

__int64 sub_1659()
{
  __int64 result; // rax
  int v1; // [rsp+Ch] [rbp-4h]

  puts("Record index:");
  result = sub_145D();
  v1 = result;
  if ( (unsigned int)result <= 0x13 )
  {
    result = (unsigned int)dword_4120[(int)result];
    if ( (_DWORD)result )
    {
      free(*((void **)&unk_4060 + v1));
      dword_4120[v1] = 0;
      return (unsigned int)--dword_4170;
    }
  }
  return result;
}

__int64 sub_16F2()
{
  __int64 result; // rax
  int v1; // [rsp+Ch] [rbp-4h]

  puts("Record index:");
  result = sub_145D();
  v1 = result;
  if ( (unsigned int)result <= 0x14 )
  {
    result = (unsigned int)dword_4120[(int)result];
    if ( (_DWORD)result )
    {
      puts("Content:");
      return write(1, *((const void **)&unk_4060 + v1), 0x130uLL);
    }
  }
  return result;
}