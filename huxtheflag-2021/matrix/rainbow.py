import hashlib
import itertools
import pickle

def generate_hash(email):
    return hashlib.sha256(email.encode()).hexdigest()

def generate_file():
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '1234567890'
    three_letters = [''.join(i) for i in itertools.product(alphabets, repeat = 3)]
    two_letters = [''.join(i) for i in itertools.product(alphabets, repeat = 2)]

    three_numbers = [''.join(i) for i in itertools.product(numbers, repeat = 3)]
    four_numbers = [''.join(i) for i in itertools.product(numbers, repeat = 4)]

    all_list = []

    for l in two_letters:
        for d in four_numbers:
            all_list.append(l + d + "@htf.ac.uk")

    for l in three_letters:
        for d in three_numbers:
            all_list.append(l + d + "@htf.ac.uk")

    hash_list = {}

    for email in all_list:
        hashed = generate_hash(email)
        hash_list[hashed] = email

    print(hash_list.get('57186caf42350e2cc3474a09ffe0ab3436885c770db36e11de404aea2f7a5cc4'))

    with open('hash_list.pickle', 'wb') as handle:
        pickle.dump(hash_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

global hash_list

with open('hash_list.pickle', 'rb') as handle:
        global hash_list
        hash_list = pickle.load(handle)
        

print(hash_list.get('66654e7da77821f2b25bbab9cf77c9cc6896c8236749aeba048e08afb3ccf744'))

# 1400 = sha256
# a=3  = bruteforce
# hashcat --hash-type=1400 --attack-mode=3 hashed ?l?l?l?d?d@ic.ac.uk -O