from pwn import *
import re

HOST, PORT = "chal.imaginaryctf.org", 42015
# context.log_level = 'critical'

def start():    
    if not args.REMOTE:
        print("Run as remote")
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    re_imaginary = re.compile(r'__import__')
    p = start()

    p.recvuntil('watch out!')
    p.recvline()
    p.recvline()

    count = 0
    while True:
        server_in = p.recvlineS()
        count += 1
        print(count)
        if ("flag" in server_in):
            p.interactive()
        elif re.search(re_imaginary, server_in):
            log.info('Evil!')
            p.sendlineafter('> ', 'ok')
            p.recvline()
        else:
            answer = (eval(server_in.replace('i', 'j'))) # WARNING: DANGEROUS
            answer2 = (str(answer)[:-1][1:]).replace('j', 'i')
            p.sendlineafter('>', answer2)
            p.recvline()

solve()