int haxor(void)

{
  byte bVar1;
  int iVar2;
  int iVar3;
  int local_24;
  int i;
  
  printf("Message ID : ");
  iVar2 = read_int();
  if ((iVar2 < 0) || (1 < iVar2)) {
    puts("[X] Invalid ID!");
    iVar2 = 0;
  }
  else if (*(long *)(ptr + (long)iVar2 * 0x10) == 0) {
    puts("[X] Message empty!");
    iVar2 = 0;
  }
  else {
    for (local_24 = 0; local_24 < 8; local_24 = local_24 + 1) {
      for (i = 0; i < *(int *)(ptr + (long)iVar2 * 0x10 + 8); i = i + 1)
      {
        bVar1 = *(byte *)((long)i + *(long *)(ptr + (long)iVar2 * 0x10));
        iVar3 = rand();
        *(byte *)((long)i + *(long *)(ptr + (long)iVar2 * 0x10)) = bVar1 ^ (byte)iVar3;
      }
    }
    printf("Encrypted Message : ");
    write(1,*(void **)(ptr + (long)iVar2 * 0x10),(ulong)*(uint *)(ptr + (long)iVar2 * 0x10 + 8));
    iVar2 = putchar(10);
  }
  return iVar2;
}