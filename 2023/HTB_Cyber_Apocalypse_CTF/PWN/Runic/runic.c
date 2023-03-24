struct {
  char[8] name; // 8 bytes
  char* malloc_address; // 8 bytes
  int size; // 8 bytes
}

unsigned __int64 create()
{
  int v1; // [rsp+0h] [rbp-20h]
  unsigned int size; // [rsp+4h] [rbp-1Ch]
  char *malloc_address; // [rsp+8h] [rbp-18h]
  __int64 name; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v5; // [rsp+18h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  name = 0LL;
  puts("Rune name: ");
  read(0, &name, 8uLL);
  v1 = hash((__int64)&name);
  if ( *(_QWORD *)(MainTable[(unsigned int)hash((__int64)&name)] + 8LL) )
  {
    puts("That rune name is already in use!");
  }
  else
  {
    puts("Rune length: ");
    size = read_int();
    if ( size <= 0x60 )
    {
      malloc_address = (char *)malloc(size + 8);
      strcpy((char *)MainTable[v1], (const char *)&name);
      *(_QWORD *)(MainTable[v1] + 8LL) = malloc_address;
      *(_DWORD *)(MainTable[v1] + 16LL) = size;
      strcpy(malloc_address, (const char *)&name);
      puts("Rune contents: ");
      read(0, malloc_address + 8, size);
    }
    else
    {
      puts("Max length is 0x60!");
    }
  }
  return __readfsqword(0x28u) ^ v5;
}

unsigned __int64 edit()
{
  int hash_new_name; // eax
  const void *malloc_address; // rbx
  int hash_new_name; // eax
  int v3; // eax
  int v4; // eax
  char *dest; // [rsp+0h] [rbp-30h]
  __int64 old_name; // [rsp+8h] [rbp-28h] BYREF
  char new_name[8]; // [rsp+10h] [rbp-20h] BYREF
  unsigned __int64 v9; // [rsp+18h] [rbp-18h]

  v9 = __readfsqword(0x28u);
  old_name = 0LL;
  *(_QWORD *)new_name = 0LL;
  puts("Rune name: ");
  read(0, &old_name, 8uLL);
  dest = *(char **)(MainTable[(unsigned int)hash((__int64)&old_name)] + 8LL);
  if ( dest )
  {
    puts("New name: ");
    read(0, new_name, 8uLL);
    if ( *(_QWORD *)(MainTable[(unsigned int)hash((__int64)new_name)] + 8LL) )
    {
      puts("That rune name is already in use!");
    }
    else
    {
      hash_new_name = hash((__int64)new_name);
      strcpy((char *)MainTable[hash_new_name], new_name);

      malloc_address = (const void *)(MainTable[(unsigned int)hash((__int64)&old_name)] + 8LL);
      hash_new_name = hash((__int64)new_name);
      memcpy((void *)(MainTable[hash_new_name] + 8LL), malloc_address, 12uLL); 

      strcpy(dest, new_name); // copy new name to malloc address

      memset((void *)MainTable[hash((__int64)&old_name)], 0, 20uLL); // clear main table old
      puts("Rune contents: ");
      v4 = hash((__int64)dest);
      read(0, dest + 8, *(unsigned int *)(MainTable[v4] + 16LL));
    }
  }
  else
  {
    puts("There's no rune with that name!");
  }
  return __readfsqword(0x28u) ^ v9;
}


unsigned __int64 delete()
{
  int v1; // [rsp+Ch] [rbp-14h]
  __int64 buf; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  buf = 0LL;
  puts("Rune name: ");
  read(0, &buf, 8uLL);
  v1 = hash((__int64)&buf);
  if ( *(_QWORD *)(MainTable[v1] + 8LL) )
  {
    free(*(void **)(MainTable[v1] + 8LL));
    memset((void *)MainTable[v1], 0, 20uLL);
    puts("Rune deleted successfully.");
  }
  else
  {
    puts("There's no rune with that name!");
  }
  return __readfsqword(0x28u) ^ v3;
}

unsigned __int64 show()
{
  int v0; // eax
  __int64 buf; // [rsp+0h] [rbp-10h] BYREF
  unsigned __int64 v3; // [rsp+8h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  buf = 0LL;
  puts("Rune name: ");
  read(0, &buf, 8uLL);
  if ( *(_QWORD *)(MainTable[(unsigned int)hash((__int64)&buf)] + 8LL) )
  {
    puts("Rune contents:\n");
    v0 = hash((__int64)&buf);
    puts((const char *)(*(_QWORD *)(MainTable[v0] + 8LL) + 8LL));
  }
  else
  {
    puts("That rune doesn't exist!");
  }
  return __readfsqword(0x28u) ^ v3;
}