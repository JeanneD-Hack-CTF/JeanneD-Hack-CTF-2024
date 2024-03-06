#!/usr/bin/python3

import hashlib
import base64

# /!\ Needs to be in wordlists (ex: rockyou.txt)
FLAG = b"capturetheflag"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:; "
SIZE = len(ALPHABET)

def main():
    # Hash the flag with SHA256
    md = hashlib.sha256()
    md.update(FLAG)
    hashed_flag = md.hexdigest()

    # Use ROT42 to encode
    msg = "Bravo pour etre arrive jusque la, mais tu ne reussiras jamais la derniere etape ! "
    msg += f"Voici le message : {hashed_flag}"

    shift = 42
    rot42 = ""
    for letter in msg:
        rot42 += ALPHABET[(ALPHABET.index(letter) + 42) % SIZE]

    # Encode again in base64
    msg = "Cette seconde étape était simple, bonne chance pour la troisième. Voici le message :\n\n"
    msg += f"{rot42}\n\n"
    msg += f"Pour t'aider, l'alphabet utilisé est le suivant :\n\n{ALPHABET}\n"

    b64 = base64.b64encode(msg.encode()).decode().replace('=','')
    
    # Finally, write result in binary
    msg = "Trop facile, passons directement à la seconde étape. Voici le message :\n\n"
    msg += f"{b64}\n"

    binary = ""
    for letter in msg:
        binary += bin(ord(letter))[2:].zfill(8)

    # Write result to file
    with open("ciphertext.bin", "w") as out:
        out.write(binary)


if __name__ == "__main__":
    main()

