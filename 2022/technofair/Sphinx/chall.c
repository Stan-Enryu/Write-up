void sphinx_labyrinth(void)

{
  char cVar1;
  uint uVar2;
  int iVar3;
  long in_FS_OFFSET;
  uint local_38;
  int local_34;
  int local_30;
  char local_28 [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_34 = 0;
  local_30 = 2;
  memset(local_28,0,0x18);
  for (local_38 = 0; local_38 < 0x18; local_38 = local_38 + 1) {
    iVar3 = rand();
    local_28[(int)local_38] = (char)iVar3;
  }
  puts("[#]  Sphinx : Alright, this is your way out. Hope we won\'t meet again.");
  puts("[#]  You    : Ofc, we won\'t meet again. \'-\')");
  puts("[%]  Leaving the room.");
  puts("\n");
  puts("===============================================================");
  puts("[#]  Sphinx : Hi, we meet again. :)");
  puts("[#]  You    : WAIT?!! HOW?! YOU\'RE LYING!");
  puts("[#]  Sphinx : Damn, I\'m lying. The one who lies is the author.");
  puts(
      "              You need to get back to the labyrinth, and you need to guess the number in each  room."
      );
  puts("              Then, I\'ll let you go.");
  puts("[#]  You    : Bruhhh... Again?!");
  puts("[#]  Sphinx : Chill.. now there are only 9 rooms");
  puts("              and I don\'t give you a limit to answer.");
  puts("[#]  You    : :/");
  puts("[#]  Sphinx : Okay okay.. I\'ll also give you 2 chances to change the numbers.");
  puts("[#]  You    : Whatever");
  puts("\n");
  while (local_34 < 10) {
    puts("===============================================================");
    puts("[!]  Quest  : Guess the number in each room");
    puts("===============================================================");
    puts("[?]  Which room that you want to guess the number (1 - 9)?");
    uVar2 = read_int("[>]  ");
    puts("\n");
    printf("[%]  Entering room %d\n",(ulong)uVar2);
    puts("[?]  1. Guess the Number");
    puts("     2. Change Number");
    iVar3 = read_int("[>]  ");
    puts("\n");
    if (iVar3 == 1) {
      puts("[?]  Give him your guess!");
      cVar1 = read_int("[>]  ");
      if (cVar1 == local_28[(int)uVar2]) {
        puts("[#]  Sphinx : Correct!");
        local_34 = local_34 + 1;
      }
      else {
        puts("[#]  Sphinx : That\'s not the correct answer.");
      }
    }
    else if ((iVar3 == 2) && (0 < local_30)) {
      puts("[?]  Enter the number you want!");
      cVar1 = read_int("[>]  ");
      local_28[(int)uVar2] = cVar1;
      local_30 = local_30 + -1;
      local_34 = local_34 + 1;
    }
    else {
      puts("[X]  Invalid choice!");
    }
    puts("[%]  Returning to the main room.");
    puts("\n");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}