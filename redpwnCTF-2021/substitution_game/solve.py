from pwn import *

HOST, PORT = "mc.ax", 31996
BINARY = 'game.py'
context.log_level = 'critical'

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(['python', 'game.py'])
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def generate_sub_string(count):
    return 'Enter substitution of form "find => replace", {} max:'.format(count)

sub_string = 'Enter substitution of form "find => replace":'
next_level_string = 'See next level? (y/n)'
add_another_string = 'Add another? (y/n)'

def solve():
    p = start()

    # Level 1
    # replace('initial', 'target')
    p.sendlineafter(next_level_string, 'y')
    p.sendlineafter(generate_sub_string(5), 'initial => target')
    p.sendlineafter(add_another_string, 'n')

    # Level 2 
    # replace('hello', 'goodbye').replace('ginkoid', 'ginky')
    p.sendlineafter(next_level_string, 'y')
    p.sendlineafter(generate_sub_string(10), 'hello => goodbye')
    p.sendlineafter(add_another_string, 'y')
    p.sendlineafter(sub_string, 'ginkoid => ginky')
    p.sendlineafter(add_another_string, 'n')

    # Level 3
    # aaaa => a
    p.sendlineafter(next_level_string, 'y')
    p.sendlineafter(generate_sub_string(10), 'aa => a')
    p.sendlineafter(add_another_string, 'n')

    # Level 4
    p.sendlineafter(next_level_string, 'y')
    p.sendlineafter(generate_sub_string(10), 'gg => ginkoid')
    p.sendlineafter(add_another_string, 'y')
    p.sendlineafter(sub_string, 'ginkoidginkoid => ginkoid')
    p.sendlineafter(add_another_string, 'y')
    p.sendlineafter(sub_string, 'ginkoidg => ginkoid')
    p.sendlineafter(add_another_string, 'n')

    # Level 5
    lvl5_answer = [('^0', '^A'),
     ('0$', 'A$'),
     ('^1', '^B'),
     ('1$', 'B$'),

     ('^A0', '^A'),
     ('0A$', 'A$'),
     ('0B$', 'A$'),
     ('^B0', '^A'),

     ('^A1', '^B'),
     ('1A$', 'B$'),
     ('1B$', 'B$'),
     ('^B1', '^B'),

     ('^AB$', 'not_palindrome'),
     ('^AA$', 'palindrome'),
     ('^BA$', 'not_palindrome'),
     ('^BB$', 'palindrome'),

     ('^A00A$', 'palindrome'),
     ('^A00B$', 'not_palindrome'),
     ('^A01A$', 'not_palindrome'),
     ('^A01B$', 'not_palindrome'),

     ('^A10A$', 'not_palindrome'),
     ('^A10B$', 'not_palindrome'),
     ('^A11A$', 'palindrome'),
     ('^A11B$', 'not_palindrome'),

     ('^B00A$', 'not_palindrome'),
     ('^B00B$', 'palindrome'),
     ('^B01A$', 'not_palindrome'),
     ('^B01B$', 'not_palindrome'),

     ('^B10A$', 'not_palindrome'),
     ('^B10B$', 'not_palindrome'),
     ('^B11A$', 'not_palindrome'),
     ('^B11B$', 'palindrome')
     ]

    p.sendlineafter(next_level_string, 'y')
    p.sendlineafter(generate_sub_string(10), 'gg => ginkoid')
    p.sendlineafter(add_another_string, 'y')
    p.sendlineafter(sub_string, 'ginkoidginkoid => ginkoid')
    p.sendlineafter(add_another_string, 'y')
    p.sendlineafter(sub_string, 'ginkoidg => ginkoid')
    p.sendlineafter(add_another_string, 'n')

    p.interactive()
    p.recvuntil('You win! Here\'s your flag:')

def test_substitution(substitutions, string):
    def substitute(s, a, b):
        initial = s
        s = s.replace(a, b)
        return (s, not s == initial)

    # s ^ 2 rounds for string of length s
    for _ in range(len(string) ** 2):
        performed_substitute = False
        print(string)
        for find, replace in substitutions:
            # print('before:', string)
            # print('replacing {f} with {r}'.format(f=find, r=replace))
            string, performed_substitute = substitute(string, find, replace)
            # print('after:', string)
            # print()
            # once a substitute is performed, go to next round
            if performed_substitute:
                break
        # if no substitute was performed this round, we are done
        if not performed_substitute:
            break
    return string


ans = test_substitution(
    [('^A00A$', 'palindrome'),
     ('^A00B$', 'not_palindrome'),
     ('^A01A$', 'not_palindrome'),
     ('^A01B$', 'not_palindrome'),

     ('^A10A$', 'not_palindrome'),
     ('^A10B$', 'not_palindrome'),
     ('^A11A$', 'palindrome'),
     ('^A11B$', 'not_palindrome'),

     ('^B00A$', 'not_palindrome'),
     ('^B00B$', 'palindrome'),
     ('^B01A$', 'not_palindrome'),
     ('^B01B$', 'not_palindrome'),

     ('^B10A$', 'not_palindrome'),
     ('^B10B$', 'not_palindrome'),
     ('^B11A$', 'not_palindrome'),
     ('^B11B$', 'palindrome'),

     ('^0', '^A'),
     ('0$', 'A$'),
     ('^1', '^B'),
     ('1$', 'B$'),

     ('^A0', '^A'),
     ('0A$', 'A$'),
     ('0B$', 'A$'),
     ('^B0', '^A'),

     ('^A1', '^B'),
     ('1A$', 'B$'),
     ('1B$', 'B$'),
     ('^B1', '^B'),

     ('^AB$', 'not_palindrome'),
     ('^AA$', 'palindrome'),
     ('^BA$', 'not_palindrome'),
     ('^BB$', 'palindrome')
     ],

    '^01101$')
print('answer:', ans)

# solve()