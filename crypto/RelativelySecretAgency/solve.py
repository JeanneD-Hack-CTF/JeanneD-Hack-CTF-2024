#!/usr/bin/python3

# ***
# Script source :
# https://xanhacks.gitlab.io/ctf-docs/crypto/rsa/08-hastad-broadcast-attack/
# ***

import base64
import os
from gmpy2 import invert, iroot, root
from Crypto.Util.number import long_to_bytes, bytes_to_long


EXPONENT = 3

keyfiles = [f"keys/key-{i}.pub" for i in range(EXPONENT)]
msgfiles = [f"encrypted/message-{i}" for i in range(EXPONENT)]


def mul(lst):
    p = 1
    for i in lst:
        p *= i
    return p


def chinese_remainder_theorem(C, N):
    assert(len(C) == len(N))
    
    # Compute N, product of the modulus
    result = 0
    modulo = mul(N)

    # Find the solution (mod N)
    for c, n in zip(C, N):
        p = modulo // n
        result += c * invert(p, n) * p

    return result % modulo


def main():
    modulus = []
    ciphertexts = []

    print("[+] Read public key modulus with openssl")
    for f in keyfiles:
        mod = os.popen(f"openssl rsa -pubin -in {f} -modulus -noout").read()
        modulus.append(int(mod.split('=')[1], 16))

    print("[+] Read and decode encrypted messages")
    for f in msgfiles:
        with open(f) as msg:
            c = msg.read()
        ciphertexts.append(bytes_to_long(base64.b64decode(c)))

    # With the chinese remainder theorem, we compute C = C_i (mod N_i)
    print("[+] Use chinese remainder theorem")
    C = chinese_remainder_theorem(ciphertexts, modulus)

    # Then, C = M³ (mod n1n2n3), so plaintext is cube root of C
    M, valid = iroot(C, EXPONENT)
    if valid:
        print("Computed M:", M)
        print("Plaintext:", long_to_bytes(M).decode())
    else:
        print("Unable to find the third root of :", C)


if __name__ == "__main__":
    main()
