from pwn import *

io = remote("saturn.picoctf.net",50305)

list_win = ["paper", "scissors", "rock"]

from ctypes import CDLL
import time, math


libc = CDLL("/usr/lib/x86_64-linux-gnu/libc-2.33.so")



# import random
# import time
# random.seed(time.time())

def print_recv():
    rec= io.recv(4096).replace("\r"," ")
    print (rec)

print_recv()

def go():
    now = int(math.floor(time.time()))
    libc.srand(now)
    io.sendline("1")
    print_recv()
    print_recv()
    io.sendline(list_win[libc.rand()%3])
    print_recv()
    print_recv()

for i in range(10):
    go()

io.interactive()