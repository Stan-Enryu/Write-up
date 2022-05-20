
void main(void)

{
  undefined8 uVar1;
  
  setup();
  welcome();
  do {
    action_menu();
    uVar1 = read_option();
    switch(uVar1) {
    case 1:
      enter_command_control();
      break;
    case 2:
      quantum_destabilizer();
      break;
    case 3:
      combat_enemy_destroyer();
      break;
    case 4:
      intercept_c2_communication();
      break;
    case 5:
      puts("[\x1b[31m!\x1b[39m] Aborting the sabotage...");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
  } while( true );
}

unsigned __int64 enter_command_control()
{
  __int64 v1; // [rsp+8h] [rbp-18h] BYREF
  char *value; // [rsp+10h] [rbp-10h]
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);

  puts("Access to the control panel of the enemy ship is protected through a privileged ACCESS code of unpredictable size");

  if ( !getenv("ACCESS") )
    setenv("ACCESS", "DENIED", 1);

  printf("[\x1B[34m*\x1B[39m] ACCESS code length: ");
  __isoc99_scanf("%lu", &v1);
  value = (char *)Malloc(v1);

  if ( !value )
  {
    puts("[\x1B[31m!\x1B[39m] Connection is lost, quantum noise is disrupting the transmission.\n");
    exit(-1);
  }

  printf("[\x1B[34m*\x1B[39m] ACCESS code: ");
  readBuffer(value, v1);
  setenv("ACCESS", value, 1);
  system("panel");
  return __readfsqword(0x28u) ^ v3;
}

unsigned __int64 quantum_destabilizer()
{
  size_t v0; // rax
  int fd; // [rsp+4h] [rbp-6Ch]
  char *string; // [rsp+8h] [rbp-68h]
  char *v4; // [rsp+10h] [rbp-60h]
  char s[8]; // [rsp+18h] [rbp-58h] BYREF
  char dest[32]; // [rsp+20h] [rbp-50h] BYREF
  char buf[40]; // [rsp+40h] [rbp-30h] BYREF
  unsigned __int64 v8; // [rsp+68h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  if ( !getenv("ACCESS") )
  {
    string = (char *)Malloc(24LL);
    strcpy(string, "ACCESS=DENIED");
    putenv(string);
  }
  
  printf("[\x1B[34m*\x1B[39m] Quantum destabilizer mount point: ");
  fgets(s, 8, stdin); //INPUT

  if ( strchr(s, '.') || strchr(s, '/') )
  {
    puts("[\x1B[31m!\x1B[39m] Thanatos spotted the intrusion, you are shot with a deadly lazer beam.");
    exit(-1);
  }
  v4 = strchr(s, 10);
  if ( v4 )
    *v4 = 0;
  memset(dest, 0, sizeof(dest));
  strcpy(dest, "/tmp/");
  strcat(dest, s);
  fd = open(dest, 66, 511LL);
  if ( fd == -1 )
  {
    puts("[\x1B[31m!\x1B[39m] Quantum destabilizer failed to penetrate the shield.");
    exit(-1);
  }
  printf("[\x1B[34m*\x1B[39m] Quantum destablizer is ready to pass a small armed unit through the enemy's shield: ");
  fgets(buf, 32, stdin); //INPUT

  v0 = strlen(buf);
  write(fd, buf, v0);
  close(fd);
  puts("[\x1B[32m+\x1B[39m] Quantum destabilizer successfully destablized Thanatos shield.");
  penetrated_the_shield = 1;
  return __readfsqword(0x28u) ^ v8;
}

void __noreturn combat_enemy_destroyer()
{
  unsigned __int64 option; // rax
  int v1; // [rsp+Ch] [rbp-14h]
  int v2; // [rsp+10h] [rbp-10h]
  int v3; // [rsp+14h] [rbp-Ch]

  v1 = 1000;
  v2 = 100000000;
  v3 = 40;
  puts("[\x1B[34m*\x1B[39m] Approaching Thanatos for a direct combat fight.");
  if ( !penetrated_the_shield )
  {
    puts("[\x1B[34m*\x1B[39m] Thanatos has a protective shield.");
    v3 = 5;
  }
  while ( 1 )
  {
    if ( v1 > 0 )
      printf("[\x1B[34m*\x1B[39m] Bonnie Health: \x1B[32m%d\x1B[39m\n", (unsigned int)v1);
    else
      printf("[\x1B[34m*\x1B[39m] Bonnie Health: \x1B[31m%d\x1B[39m\n", (unsigned int)v1);
    if ( v2 > 1000 )
      printf("[\x1B[34m*\x1B[39m] Thanatos Health: \x1B[32m%d\x1B[39m\n", (unsigned int)v2);
    else
      printf("[\x1B[34m*\x1B[39m] Thanatos Health: \x1B[31m%d\x1B[39m\n", (unsigned int)v2);
    puts("\n");
    if ( v1 <= 0 )
      break;
    if ( v2 <= 0 )
    {
      puts("[\x1B[32m+\x1B[39m] Thanatos is \x1B[31mdestroyed\x1B[39m!");
      puts("[\x1B[32m+\x1B[39m] Mission accomplished!");
      exit(-559038737);
    }
    weaponry_menu();
    option = read_option();
    if ( option == 2 )
    {
      v2 += -30 * v3;
    }
    else if ( option > 2 )
    {
      if ( option == 3 )
      {
        v2 += -15 * v3;
      }
      else if ( option == 4 )
      {
        v2 += -10 * v3;
      }
    }
    else if ( option == 1 )
    {
      v2 += -20 * v3;
    }
    v1 -= 80 * (rand() % 30);
  }
  puts("[\x1B[31m!\x1B[39m] You are \x1B[31mannihilated\x1B[39m.");
  exit(0);
}

unsigned __int64 intercept_c2_communication()
{
  int v0; // eax
  unsigned int buf; // [rsp+8h] [rbp-58h] BYREF
  int i; // [rsp+Ch] [rbp-54h]
  int j; // [rsp+10h] [rbp-50h]
  int fd; // [rsp+14h] [rbp-4Ch]
  int v6; // [rsp+18h] [rbp-48h]
  const char *v8; // [rsp+20h] [rbp-40h]
  const char *v9; // [rsp+28h] [rbp-38h]
  char v10[40]; // [rsp+30h] [rbp-30h] BYREF
  unsigned __int64 v11; // [rsp+58h] [rbp-8h]

  v11 = __readfsqword(0x28u);
  fd = open("/dev/urandom", 0);
  v8 = 0LL;
  v9 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!-./:;<=>?@[\\]^_`{|}~";
  
  puts(
    "[\x1B[34m*\x1B[39m] Intercepting Thanatos communication with the command center, but unfortunately they use quantum encryption.");
  read(fd, &buf, 4uLL);
  srand(buf);
  v6 = rand() % 10;
  if ( !v6 )
    puts("[\x1B[31m!\x1B[39m] No message is intercepted!");
  for ( i = 0; i < v6; ++i )
  {
    if ( rand() % 2 )
      v8 = "C2C";
    else
      v8 = "Enemy";
    read(fd, v10, 0x1FuLL);
    for ( j = 0; j <= 30; ++j )
      v10[j] = v9[(unsigned __int8)v10[j] % 0x53u];
    v10[31] = 0;
    printf("\n[\x1B[32m%s\x1B[39m] %s\n", v8, v10);

    v0 = rand();
    sleep(v0 % 3);
  }
  puts(&byte_1F7F);
  close(fd);
  return __readfsqword(0x28u) ^ v11;
}


__int64 read_option()
{
  char *s; // [rsp+0h] [rbp-10h]
  __int64 v2; // [rsp+8h] [rbp-8h]

  s = (char *)Malloc(16LL);
  printf("> ");
  fgets(s, 16, stdin);
  v2 = strtol(s, 0LL, 0);
  Free(s);
  return v2;
}

void __fastcall Free(__int64 a1)
{
  free((void *)(a1 - 8));
}

unsigned __int64 __fastcall readBuffer(__int64 a1, unsigned __int64 a2)
{
  unsigned __int64 result; // rax
  unsigned __int64 i; // [rsp+18h] [rbp-8h]

  for ( i = 0LL; ; ++i )
  {
    result = i;
    if ( i >= a2 )
      break;
    read(0, (void *)(a1 + i), 1uLL);
    result = *(unsigned __int8 *)(a1 + i);
    if ( !(_BYTE)result )
      break;
    if ( *(_BYTE *)(a1 + i) == '\n' )
    {
      result = a1 + i;
      *(_BYTE *)(a1 + i) = 0;
      return result;
    }
  }
  return result;
}

long * Malloc(long param_1)

{
  long *plVar1;
  
  plVar1 = (long *)malloc(param_1 + 8);
  if (plVar1 == (long *)0x0) {
    plVar1 = (long *)0x0;
  }
  else {
    *plVar1 = param_1;
    plVar1 = plVar1 + 1;
  }
  return plVar1;
}