int __cdecl main(int argc, const char **argv, const char **envp)
{
  setvbuf(stderr, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  robots_factory();
  return 0;
}

__int64 robots_factory()
{
  int v1; // [rsp+Ch] [rbp-4h]

  puts("Welcome to the secret robots factory!");
  while ( 1 )
  {
    menu();
    v1 = read_int();
    if ( v1 == 4 )
      break;
    if ( v1 <= 4 )
    {
      switch ( v1 )
      {
        case 3:
          destroy_robot();
          break;
        case 1:
          new_robot();
          break;
        case 2:
          program_robot();
          break;
      }
    }
  }
  return 0LL;
}

unsigned __int64 new_robot()
{
  int i; // [rsp+8h] [rbp-18h]
  int v2; // [rsp+Ch] [rbp-14h]
  char buf[5]; // [rsp+13h] [rbp-Dh] BYREF
  unsigned __int64 v4; // [rsp+18h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  if ( number_robots <= 4 )
  {
    puts("Provide robot memory size:");
    read(0, buf, 4uLL);
    v2 = atoi(buf);
    if ( v2 > 256 )
    {
      for ( i = 0; i <= 4; ++i )
      {
        if ( !check_robot_slot[i] )
        {
          robots[i] = calloc(1uLL, v2);
          check_robot_slot[i] = 1;
          robot_memory_size[i] = v2;
          printf("You got new page at index %d\n", (unsigned int)i);
          ++number_robots;
          return __readfsqword(0x28u) ^ v4;
        }
      }
    }
    else
    {
      puts("you're creating a stupid robot.");
    }
  }
  else
  {
    puts("All slots are occupied :(");
  }
  return __readfsqword(0x28u) ^ v4;
}

unsigned __int64 program_robot()
{
  unsigned int v1; // [rsp+Ch] [rbp-14h]
  char buf[5]; // [rsp+13h] [rbp-Dh] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  puts("Provide robot's slot:");
  read(0, buf, 4uLL);
  v1 = atoi(buf);
  if ( v1 > 4 )
  {
    puts("Slot is empty!");
  }
  else if ( robots[v1] )
  {
    puts("Program the robot:");
    read(0, (void *)robots[v1], (int)robot_memory_size[v1]);
  }
  return __readfsqword(0x28u) ^ v3;
}

unsigned __int64 destroy_robot()
{
  int v1; // [rsp+Ch] [rbp-14h]
  char buf[5]; // [rsp+13h] [rbp-Dh] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  puts("Provide robot's slot:");
  read(0, buf, 4uLL);
  v1 = atoi(buf);
  if ( (unsigned int)v1 > 4 )
  {
    puts("Slot is empty!");
  }
  else if ( check_robot_slot[v1] )
  {
    free(*((void **)&robots + v1));
    check_robot_slot[v1] = 0;
    --number_robots;
  }
  else
  {
    puts("robot doesn't exist!");
  }
  return __readfsqword(0x28u) ^ v3;
}

ssize_t menu()
{
  puts("1- Create a robot");
  puts("2- Program a robot");
  puts("3- Destroy a robot");
  puts("4- Exit");
  return write(1, "> ", 2uLL);
}

__int64 read_int()
{
  char buf[5]; // [rsp+13h] [rbp-Dh] BYREF
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  read(0, buf, 4uLL);
  return (unsigned int)atoi(buf);
}