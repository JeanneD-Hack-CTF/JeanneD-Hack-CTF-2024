import ctypes
import subprocess

KEY_SIZE = 32

ALPHABET = [
    0x62, 0x6d, 0x50, 0x78, 0x46, 0x76, 0x71, 0x4c,
    0x75, 0x35, 0x49, 0x58, 0x4d, 0x52, 0x37, 0x47,
    0x34, 0x36, 0x6b, 0x73, 0x70, 0x77, 0x32, 0x48,
    0x7a, 0x66, 0x72, 0x4f, 0x69, 0x68, 0x63, 0x55,
    0x6f, 0x4e, 0x56, 0x45, 0x31, 0x64, 0x30, 0x38,
    0x6c, 0x6e, 0x44, 0x53, 0x43, 0x5a, 0x33, 0x61,
    0x54, 0x4a, 0x79, 0x57, 0x42, 0x51, 0x39, 0x67,
    0x65, 0x6a, 0x59, 0x4b, 0x74, 0x41
]

def main():
    libc = ctypes.CDLL("libc.so.6")
    seed = libc.time(None)
    libc.srandom(seed)
    filename = ''
    for i in range(KEY_SIZE):
        value = libc.random() % len(ALPHABET)
        filename += chr(ALPHABET[value])

    open(filename, 'w').close()
    subprocess.run(['./keygen', 'test'])
    subprocess.run(['cat', filename])
    subprocess.run(['rm', filename])

if __name__ == '__main__':
    main()
