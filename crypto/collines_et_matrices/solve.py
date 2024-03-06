#!/usr/bin/env python3

import re
import socket
import string

from time import sleep
from pprint import pprint
from sympy import Matrix

HOST = "127.0.0.1"
# HOST = "142.93.36.168"
PORT = 50001

"""
Après avoir compris qu'il s'agit d'un chiffrement de Hill, il nous faut calculer la matrice
de déchiffrement. Pour cela il suffit de calculer l'inverse de la matrice de chiffrement
modulo 25 (taille de l'alphabet).
On peut retrouver la matrice de chiffrement en envoyant certains messages.

'a' = 0, une fois converti en nombre et sert de padding dans le message.
'b' = 1, et correspond donc à l'élément neutre.

Le message 'baaaa' correspond donc au vecteur (1,0,0,0,0) et permet de récupérer la 1ère colonne
de la matrice de chiffrement avec le produit matrice vecteur.
Avec le message 'abaaa' on peut de la même  façon retrouver le seconde colonne, etc...
"""

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    welcome = s.recv(1024).decode()
    ciphertext = re.search("le message à déchiffrer : ([a-y]+)", welcome).group(1)
    print("[+] Ciphertext to decrypt: ", ciphertext)

    ciphertexts = []
    
    print("[+] Retrieve ciphertexts messages")
    sleep(0.5)

    for msg in ["baaaa", "abaaa", "aabaa", "aaaba", "aaaab"]:
        s.sendall(f"{msg}\n".encode())
        sleep(0.5)
        resp = s.recv(1024).decode()
        r = re.search(r"Message chiffré : ([a-y]{5})", resp)
        ciphertexts.append(r.group(1))
        sleep(0.5)

    print("[+] Build Hill cipher matrix")

    alph = string.ascii_lowercase[:-1]
    size = len(alph)
    matrix = [[], [], [], [], []]
    line = 0

    for column in ciphertexts:
        vect = [alph.index(c) for c in column]
        for i in range(5):
            matrix[i].append(vect[i])

    M = Matrix(matrix)    
    pprint(M)

    print("[+] Compute the inverse of the matrix")

    invM = M.inv_mod(size)
    pprint(invM)

    print("[+] Decrypt ciphertext")

    flag = ''
    for chunk in [ciphertext[i:i+5] for i in range(0, len(ciphertext), 5)]:
        vect = Matrix([alph.index(c) for c in chunk])
        plain = invM * vect
        flag += ''.join(alph[i % size] for i in plain)

    print("Flag:", flag)

    s.close()


if __name__ == "__main__":
    solve()
