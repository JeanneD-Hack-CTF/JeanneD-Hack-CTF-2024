import random

def corrupt(data, start, end):
    for i in range(start, end):
        data[i] = 0xff if random.randint(0, 1) else 0x00

def main():
    with open('zephyr.bin', 'rb') as fp:
        data = bytearray(fp.read())
        # Replace start and end by 0xff, using random offset
        # The main point is that binbloom && file should return 
        # correct informations
        corrupt(data, 0x00142, 0xffe8)
        corrupt(data, 0x10500, 0x10854) # This part hide the verification of the admin flag
        corrupt(data, 0x128f4, 0x2490f)
        corrupt(data, 0x26014, len(data))
        with open('corrupted.bin', 'wb') as out:
            out.write(data)

if __name__ == '__main__':
    main()
