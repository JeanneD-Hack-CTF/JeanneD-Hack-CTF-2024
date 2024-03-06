#!/usr/bin/env python3

from string import ascii_lowercase
from random import shuffle


FLAG_FILE = "flag.txt"
ENC_FLAG = "encrypted.txt"


def encrypt(msg, src_alph, dest_alph):
    enc = ""
    for letter in msg:
        if letter in src_alph:
            enc += dest_alph[src_alph.index(letter)]
        else:
            enc += letter
    return enc


def main():
    alph = [l for l in ascii_lowercase]
    cipher_alph = alph.copy()
    shuffle(cipher_alph)

    print("Alphabet:", alph)
    print("Substitution:", cipher_alph)

    with open(FLAG_FILE, 'r') as flag_f:
        flag = flag_f.read()

    enc_flag = encrypt(flag, alph, cipher_alph)
    print("Flag:", enc_flag)

    with open(ENC_FLAG, 'w') as out:
        out.write(enc_flag)


if __name__ == "__main__":
    main()
