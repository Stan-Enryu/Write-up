
void main(void)

{
  int iVar1;
  uint uVar2;
  undefined8 uVar3;
  long lVar4;
  void *__ptr;
  
  setbuf(stdin,(char *)0x0);
  setbuf(stdout,(char *)0x0);
  do {
    iVar1 = get_num(menu);
    uVar2 = get_num("idx? ");
    if (7 < uVar2) {
                    /* WARNING: Subroutine does not return */
      __assert_fail("idx < NUM_QUEUES","queue.c",0x5f,(char *)&__PRETTY_FUNCTION__.3070);
    }
    if (iVar1 < 6) {
      switch(iVar1) {
      case 1:
        uVar3 = queue_create(strcmp);
        *(undefined8 *)(qs + (ulong)uVar2 * 8) = uVar3;
        break;
      case 2:
        if (*(long *)(qs + (ulong)uVar2 * 8) == 0) {
                    /* WARNING: Subroutine does not return */
          __assert_fail("qs[idx]","queue.c",0x65,(char *)&__PRETTY_FUNCTION__.3070);
        }
        queue_free(*(undefined8 *)(qs + (ulong)uVar2 * 8));
        *(undefined8 *)(qs + (ulong)uVar2 * 8) = 0;
        break;
      case 3:
        if (*(long *)(qs + (ulong)uVar2 * 8) == 0) {
                    /* WARNING: Subroutine does not return */
          __assert_fail("qs[idx]","queue.c",0x6a,(char *)&__PRETTY_FUNCTION__.3070);
        }
        lVar4 = get_string("content? ");
        if (lVar4 == 0) {
                    /* WARNING: Subroutine does not return */
          __assert_fail("item","queue.c",0x6c,(char *)&__PRETTY_FUNCTION__.3070);
        }
        queue_push(*(undefined8 *)(qs + (ulong)uVar2 * 8),lVar4);
        break;
      case 4:
        if (*(long *)(qs + (ulong)uVar2 * 8) == 0) {
                    /* WARNING: Subroutine does not return */
          __assert_fail("qs[idx]","queue.c",0x70,(char *)&__PRETTY_FUNCTION__.3070);
        }
        __ptr = (void *)queue_pop(*(undefined8 *)(qs + (ulong)uVar2 * 8));
        printf("item: %s\n",__ptr);
        free(__ptr);
        break;
      case 5:
        if (*(long *)(qs + (ulong)uVar2 * 8) == 0) {
                    /* WARNING: Subroutine does not return */
          __assert_fail("qs[idx]","queue.c",0x76,(char *)&__PRETTY_FUNCTION__.3070);
        }
        queue_compact(*(undefined8 *)(qs + (ulong)uVar2 * 8));
      }
    }
    else if (iVar1 == 69) {
      if (*(long *)(qs + (ulong)uVar2 * 8) == 0) {
                    /* WARNING: Subroutine does not return */
        __assert_fail("qs[idx]","queue.c",0x7a,(char *)&__PRETTY_FUNCTION__.3070);
      }
      printf("data: %p\nlength: %zu\nsize: %zu\ncmp: %p\n",**(undefined8 **)(qs + (ulong)uVar2 * 8),
             *(undefined8 *)(*(long *)(qs + (ulong)uVar2 * 8) + 8),
             *(undefined8 *)(*(long *)(qs + (ulong)uVar2 * 8) + 0x10),
             *(undefined8 *)(*(long *)(qs + (ulong)uVar2 * 8) + 0x18));
    }
    fputc(10,stdout);
  } while( true );
}


void ** queue_create(void *strcmp)

{
  void **qs_temp;
  void *pvVar2;
  
  qs_temp = (void **)malloc(0x20);

  if (qs_temp == (void **)0x0) {
    __assert_fail("q","queue.c",0x11,"queue_create");
  }
  qs_temp.max_len_queue = (void *)0x8;

  pvVar2 = malloc(64);
  qs_temp.address_queue = pvVar2;

  if (*qs_temp == (void *)0x0) {
    __assert_fail("q->data","queue.c",0x14,"queue_create");
  }
  qs_temp.len_queue = (void *)0x0;
  qs_temp.address_strcmp = strcmp;
  return qs_temp;
}


void queue_free(void **qs_temp)

{
  free(qs_temp.address_queue);
  free(qs_temp);
  return;
}


void queue_push(void **qs_temp,undefined8 param_2){
  int iVar1;
  void *pvVar2;
  void *local_10;
  
  if (qs_temp.max_len_queue == qs_temp.len_queue ) {
    qs_temp.max_len_queue = (void *)((long)qs_temp.max_len_queue * 2);
    pvVar2 = realloc(qs_temp.address_queue, (long)qs_temp.max_len_queue * 8);
    qs_temp.address_queue = pvVar2;
  }
  for (local_10 = qs_temp.len_queue ; local_10 != (void *)0x0; local_10 = (void *)((long)local_10 - 1)) {
    iVar1 = (*(code *)qs_temp.address_strcmp)(param_2,*(undefined8 *)((long)*qs_temp + (long)local_10 * 8 - 8)) ;
    if (iVar1 < 0) break;

    *(undefined8 *)((long)*qs_temp + (long)local_10 * 8 ) = *(undefined8 *)((long)*qs_temp + (long)local_10 * 8 - 8);
  }
  *(undefined8 *)((long)local_10 * 8 + (long)*qs_temp) = param_2;
  qs_temp[1] = (void *)((long)qs_temp[1] + 1);
  return;
}


undefined8 queue_pop(long *param_1)

{
  if (param_1[1] == 0) {
                    /* WARNING: Subroutine does not return */
    __assert_fail("q->length > 0","queue.c",0x30,"queue_pop");
  }
  param_1[1] = param_1[1] -1;
  return *(undefined8 *)(param_1[1] * 8 + *param_1);
}


void queue_compact(void **param_1)

{
  void *pvVar1;
  
  param_1.max_len_queue = param_1.len_queue;
  pvVar1 = realloc(*param_1,(long)param_1[2] * 8);
  *param_1 = pvVar1;
  return;
}

