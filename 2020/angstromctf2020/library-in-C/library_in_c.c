
undefined8 main(void)

{
  __gid_t __rgid;
  long in_FS_OFFSET;
  char local_98 [64];
  char local_58 [72];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdout,(char *)0x0,2,0);
  __rgid = getegid();
  setresgid(__rgid,__rgid,__rgid);
  puts("Welcome to the LIBrary in C!");
  puts("What is your name?");
  fgets(local_98,64,stdin);
  printf("Why hello there ");
  printf(local_98);
  puts("And what book would you like to check out?");
  fgets(local_58,64,stdin);
  printf("Your cart:\n - ");
  printf(local_58);
  puts("\nThat\'s great and all but uh...");
  puts("It turns out this library doesn\'t actually exist so you\'ll never get your book.");
  puts("Have a nice day!");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

