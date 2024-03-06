#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define ERROR       -42
#define SUCCESS       0

#define KEY_SIZE     32

unsigned char PREF[6] = { 0xDB, 0xEE, 0x69, 0x6C, 0x76, 0xB8 };

int write_flag(char *filename) {
    FILE *f = fopen(filename, "w");
    if (f == NULL) {
        return ERROR;
    }

    for (unsigned int i = 0, v = 0; i < 6; i++)
    {
            v = PREF[i];
            v = ((v << 1) | ( (v & 0xFF) >> 7)) & 0xFF;
            v -= 0x71;
            PREF[i] = v;
    }
    fwrite(PREF, 1, sizeof(PREF), f);

    unsigned char a[8] = { 0x44, 0x82, 0x84, 0x9A, 0xFB, 0xCC, 0x82, 0x01 };
    unsigned char b[8] = { 0xEC, 0xC0, 0xDA, 0x64, 0xD8, 0x68, 0xC0, 0x02 };
    unsigned char c[7] = { 0x3C, 0x75, 0x2C, 0x72, 0x70, 0x3C, 0xA1 };

    for (int j = -0xd * 0x147 + 0x785 * -0x3 + -0x2 * -0x1395; j < 0x1 * 0x1b0a + 0x3 * -0x769 + 0x133 * -0x4; ++j) 
    {
        if (j == 0x813 + -0xcb9 + 0x4a7) 
        {
            for (unsigned int i = 0, v = 0; i < 8; i++)
            {
                    v = b[i];
                    v = (((v & 0xFF) >> 1) | (v << 7)) & 0xFF;
                    v --;
                    b[i] = v;
            }
            fwrite(b, 1, sizeof(b), f);
        }

        if (j == -0x8 * -0x8 + 0x1 * 0x22eb + -0x232b) 
        {
            for (unsigned int i = 0, v = 0; i < 8; i++)
            {
                    v = a[i];
                    v --;
                    v = (((v & 0xFF) >> 3) | (v << 5)) & 0xFF;
                    a[i] = v;
            }
            fwrite(a, 1, sizeof(a), f);
        }

        if (j == -0x87d + 0xdb6 + -0x537) 
        {
            for (unsigned int i = 0, v = 0; i < 7; i++)
            {
                    v = c[i];
                    v ^= i;
                    v = ~v;
                    v += 0xA8;
                    c[i] = v;
            }
            fwrite(c, 1, sizeof(c), f);
        }
    }

    fwrite("}", 1, 1, f);
    fclose(f);
    return SUCCESS;
} 

int check_password(char *password) {
    unsigned char alphabet[] = {
        0x62, 0x6d, 0x50, 0x78, 0x46, 0x76, 0x71, 0x4c, 
        0x75, 0x35, 0x49, 0x58, 0x4d, 0x52, 0x37, 0x47, 
        0x34, 0x36, 0x6b, 0x73, 0x70, 0x77, 0x32, 0x48, 
        0x7a, 0x66, 0x72, 0x4f, 0x69, 0x68, 0x63, 0x55, 
        0x6f, 0x4e, 0x56, 0x45, 0x31, 0x64, 0x30, 0x38, 
        0x6c, 0x6e, 0x44, 0x53, 0x43, 0x5a, 0x33, 0x61, 
        0x54, 0x4a, 0x79, 0x57, 0x42, 0x51, 0x39, 0x67, 
        0x65, 0x6a, 0x59, 0x4b, 0x74, 0x41
    };
    size_t seed = time(NULL);
    srandom(seed); 
    char filename[KEY_SIZE];
    for (int i = 0; i < KEY_SIZE; i++) {
        int value = random() % sizeof(alphabet);
        filename[i] = alphabet[value];
    }
    filename[KEY_SIZE] = 0;
    // Wait a bit to be sure that access will detect newly created file
    sleep(1);
    // Check if file exists
    if (access(filename, F_OK) != 0) {
        return ERROR;
    }
    return write_flag(filename);
}

// Flag: Flag{h0p3_y0u_l1k3_k3y63n}
int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <password>\n", argv[0]);
        return ERROR;
    }
    if (check_password(argv[1]) != SUCCESS) {
        printf("Wrong password\n");
        return ERROR; 
    }
    return SUCCESS;
}
