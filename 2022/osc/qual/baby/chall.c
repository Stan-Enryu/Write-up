int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  __int64 v4; // rbx
  __int64 v5; // rdx
  unsigned int v6; // eax
  void *v7; // rax
  __int64 v8; // rdx
  __int64 v9; // rax
  size_t v10; // rbx
  void **v11; // rax
  _QWORD *v12; // rax
  const char **v13; // rax
  __int64 v14; // rdx
  __int64 v15; // rax
  __int64 v16; // rax
  unsigned int v18; // [rsp+4h] [rbp-14Ch] BYREF
  unsigned int v19; // [rsp+8h] [rbp-148h] BYREF
  int v20; // [rsp+Ch] [rbp-144h]
  char v21[32]; // [rsp+10h] [rbp-140h] BYREF
  char v22[264]; // [rsp+30h] [rbp-120h] BYREF
  unsigned __int64 v23; // [rsp+138h] [rbp-18h]

  v23 = __readfsqword(0x28u);
  alarm(0x3Cu);
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
  std::string::basic_string(v21);
  v18 = 0;
  v19 = 0;
  memset(v22, 0, 0x100uLL);
  v3 = std::operator<<<std::char_traits<char>>(&std::cout, "Hello World!", v22);
  std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
  while ( 1 )
  {
    while ( 1 )
    {
      while ( 1 )
      {
        while ( 1 )
        {
          while ( 1 )
          {
            my_cin<std::string>("Options:\n- add\n- remove\n- read\n- send\n- quit\n", v21);
            if ( !(unsigned __int8)std::operator==<char>(v21, "add") )
              break;
            my_cin<unsigned int>("Index: ", &v18);
            my_cin<unsigned int>("Size: ", &v19);
            v4 = std::array<String,16ul>::at(v22, v18);
            v5 = operator new[](v19);
            v6 = v19;
            *(_QWORD *)v4 = v5;
            *(_DWORD *)(v4 + 8) = v6;
          }
          if ( !(unsigned __int8)std::operator==<char>(v21, "remove") )
            break;
          my_cin<unsigned int>("Index: ", &v18);
          v7 = *(void **)std::array<String,16ul>::at(v22, v18);
          if ( v7 )
            operator delete[](v7);
        }
        if ( !(unsigned __int8)std::operator==<char>(v21, "send") )
          break;
        my_cin<unsigned int>("Index: ", &v18);
        v9 = std::operator<<<std::char_traits<char>>(&std::cout, "Send message: ", v8);
        std::ostream::operator<<(v9, &std::endl<char,std::char_traits<char>>);
        v10 = (unsigned int)(*(_DWORD *)(std::array<String,16ul>::at(v22, v18) + 8) - 1);
        v11 = (void **)std::array<String,16ul>::at(v22, v18);
        v20 = read(0, *v11, v10);
        v12 = (_QWORD *)std::array<String,16ul>::at(v22, v18);
        *(_BYTE *)(*v12 + v20 + 1LL) = 0;
      }
      if ( !(unsigned __int8)std::operator==<char>(v21, "read") )
        break;
      my_cin<unsigned int>("Index: ", &v18);
      v13 = (const char **)std::array<String,16ul>::at(v22, v18);
      puts(*v13);
    }
    if ( (unsigned __int8)std::operator==<char>(v21, "quit") )
      break;
    v16 = std::operator<<<std::char_traits<char>>(&std::cout, "Try again", v14);
    std::ostream::operator<<(v16, &std::endl<char,std::char_traits<char>>);
  }
  v15 = std::operator<<<std::char_traits<char>>(&std::cout, "Goodbye World!", v14);
  std::ostream::operator<<(v15, &std::endl<char,std::char_traits<char>>);
  std::string::~string(v21);
  return 0;
}s