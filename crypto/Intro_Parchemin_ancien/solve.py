#!/usr/bin/env python3

import string
from pprint import pprint


ENCRYPTED = 'encrypted.txt'

# Compute frequency analysis of encrypted text
def freq_analysis(enc):
    freqs = {}
    alph = string.ascii_lowercase
    # Initialize dictionary
    for l in alph:
        freqs[l] = 0

    # Count occurences of each letter
    for l in enc:
        if l in alph:
            freqs[l] += 1

    # Compute the percent of each letter in the text
    length = len(enc)
    for k,v in freqs.items():
        freqs[k] = round((v / length) * 100, 3)

    # Return freqs sorted by percentage
    return dict(sorted(freqs.items(), key=lambda x:x[1], reverse=True))


# Return default french freqs (from statistics)
def french_freqs():
    stats_freqs = {
        "a": 8.15,
        "b": 0.97,
        "c": 3.15,
        "d": 3.73,
        "e": 17.39,
        "f": 1.12,
        "g": 0.97,
        "h": 0.85,
        "i": 7.31,
        "j": 0.45,
        "k": 0.02,
        "l": 5.69,
        "m": 2.87, 
        "n": 7.12,
        "o": 5.28,
        "p": 2.80,
        "q": 1.21,
        "r": 6.64,
        "s": 8.14,
        "t": 7.22,
        "u": 6.38,
        "v": 1.64,
        "w": 0.03,
        "x": 0.41,
        "y": 0.28,
        "z": 0.15,
    }
    # Sort in the same way as the computed frequency analysis
    sorted_freqs = sorted(stats_freqs.items(), key=lambda x:x[1], reverse=True)
    return dict(sorted_freqs)


def encrypt(msg, original, substitution):
    enc = ""
    for letter in msg:
        if letter in original:
            enc += substitution[original.index(letter)]
        else:
            enc += letter
    return enc


# Solve substitution
def solve():
    enc = ""
    with open(ENCRYPTED, 'r') as encf:
        enc = encf.read()

    # Compute frenquencies
    print("[+] Ciphertext frequency analysis (in percent):")
    enc_freqs = freq_analysis(enc)
    pprint(enc_freqs)

    print("[+] Frequency analysis of French language (statistics, in percent):")
    default_french = french_freqs()
    pprint(default_french)

    # Apply modifications
    enc_alph, french_alph = ''.join(enc_freqs.keys()), ''.join(default_french.keys())
    print(enc_alph, french_alph)
    print("[+] Decrypted text:", encrypt(enc, enc_alph, french_alph))



if __name__ == "__main__":
    # Try to solve with Python and frequency analysis
    solve()
    # or
    # go to https://dcode.fr/monoalphabetic-substitution
