from pwn import *
import re

HOST, PORT = "192.168.125.111", 9003
context.log_level = 'critical'

def load_file():
    print("Loading file")
    with open('hash_list.pickle', 'rb') as handle:
        global hash_list
        hash_list = pickle.load(handle)
    print("Done loading file")

def start():
    return remote(HOST, PORT)

def calc(guess, num):
    return str((guess * (666013) ** 3) % num)

def guess():
    global hash_list
    p = start()

    payload = 'blue'
    p.sendlineafter("choose?", payload)

    # Calculate HTF tags
    p.recvregex('% (%d)*')
    num = int(p.recvline())
    p.sendline(calc(1158, num))
    response = str(p.recvline())
    
    # Calculate hashes
    p.recvuntil("Good luck!\n")

    try:
        for i in range(0, 20):
            hashed = str(p.recvline().decode()[:-1]) # Remove new line character
            print(hashed)
            cracked = hash_list.get(hashed)
            p.sendline(cracked)
            print(cracked)
    except AttributeError:
        print("Done!")
    
    p.interactive()

load_file()
guess()

#HTF{h0w_d1d_u_brut3_f0rc3_sha256_l0l_gg}