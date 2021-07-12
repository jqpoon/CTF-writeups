import random

key = random.randint(0, 25)
enc = "egddagzp_ftue_rxms_iuft_rxms_radymf"

def solve(key):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted = alphabet[key:] + alphabet[:key]
    dictionary = dict(zip(alphabet, shifted))

    print(''.join([
        dictionary[c]
        if c in dictionary
        else c
        for c in enc
    ]))

for key in range(0, 25):
    solve(key)