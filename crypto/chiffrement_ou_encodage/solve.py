#!/usr/bin/python3

import re
import base64

ciphertext = open('projetjeanne.bin', 'r').read()


def rot_decode(msg, shift, alphabet):
    dec = ''
    size = len(alphabet)
    for letter in msg:
        dec += alphabet[(alphabet.index(letter) - shift) % size]
    return dec


def main():
    # Decode from binary
    msg = ''.join([chr(int(b, 2)) for b in [ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)]])
    print("Step 1:\n", msg)

    # Decode from base64
    b64 = msg.split('\n')[2]
    b64_dec = base64.b64decode(b64).decode()
    print("Step 2:\n", b64_dec)

    # Brute force ROT
    rot = b64_dec.split('\n')[2]
    alphabet = b64_dec.split('\n')[6]
    size = len(alphabet)
    
    for i in range(size):
        rot_dec = rot_decode(rot, i, alphabet)
        if "Voici le message" in rot_dec:
            clear = rot_dec
            print("Step 3:\n", clear)
            break

    final_hash = re.search("[0-9a-f]{64}", clear).group(0)
    print("\nStep 4:")
    print(f" Crack the hash: {final_hash}")
    print(" ex.: john --format=raw-sha256 hash.txt")


if __name__ == "__main__":
    main()
