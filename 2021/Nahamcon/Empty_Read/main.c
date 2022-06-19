void add(void)
{
    int32_t iVar1;
    undefined4 uVar2;
    int32_t iVar3;
    int32_t unaff_EBX;
    int32_t in_GS_OFFSET;
    int32_t var_1ch;
    undefined4 size;
    undefined4 var_14h;
    char *str;
    int32_t var_ch;
    int32_t var_8h;

    fcn.000006b0();
    var_ch = *(int32_t *)(in_GS_OFFSET + 0x14);
    puts(unaff_EBX + 0x7b4);
    read(0, &str, 4);
    iVar1 = atoi(&str);
    if (((iVar1 < 0) || (9 < iVar1)) || (*(int32_t *)(unaff_EBX + 0x2788 + iVar1 * 4) != 0)) {
        puts(unaff_EBX + 0x7c8);
    } else {
        uVar2 = malloc(8);
        *(undefined4 *)(unaff_EBX + 0x2788 + iVar1 * 4) = uVar2;
        if (*(int32_t *)(unaff_EBX + 0x2788 + iVar1 * 4) == 0) {
            puts(unaff_EBX + 0x7e0);
        } else {
            memset(&str, 0, 4);
            puts(unaff_EBX + 0x802);
            read(0, &str, 4);
            var_1ch = atoi(&str);
            if ((var_1ch < 1) || (0x200 < var_1ch)) {
                var_1ch = 0x200;
            }
            **(int32_t **)(unaff_EBX + 0x2788 + iVar1 * 4) = var_1ch;
            iVar3 = *(int32_t *)(unaff_EBX + 0x2788 + iVar1 * 4);
            uVar2 = malloc(**(undefined4 **)(unaff_EBX + 0x2788 + iVar1 * 4));
            *(undefined4 *)(iVar3 + 4) = uVar2;
            if (*(int32_t *)(*(int32_t *)(unaff_EBX + 0x2788 + iVar1 * 4) + 4) == 0) {
                puts(unaff_EBX + 0x7e0);
            } else {
                puts(unaff_EBX + 0x816);
                iVar3 = read(0, (*(int32_t *)(unaff_EBX + 0x2788 + iVar1 * 4) + 4), (unaff_EBX + 0x2788 + iVar1 * 4));
                if (iVar3 < 1) {
                    **(undefined **)(*(int32_t *)(unaff_EBX + 0x2788 + iVar1 * 4) + 4) = 0;
                } else {
                    *(undefined *)(iVar3 + *(int32_t *)(*(int32_t *)(unaff_EBX + 0x2788 + iVar1 * 4) + 4)) = 0;
                }
            }
        }
    }
    if (var_ch != *(int32_t *)(in_GS_OFFSET + 0x14)) {
    // WARNING: Subroutine does not return
        fcn.00000ff0();
    }
    return;
}
