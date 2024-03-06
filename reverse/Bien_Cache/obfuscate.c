#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ERROR       -42
#define SUCCESS       0
 
int check_password(char *password) {
    const char ref[] = {
        0x3a, 0x72, 0x30, 0x1d, 0x2f, 0x71, 0x1d, 0x24, 0x72, 0x30, 0x1d, 0x75, 0x2a, 0x71, 0x1d, 0x35, 0x73, 0x2c
    };
    size_t len = strlen(password); 
    if (len != sizeof(ref)) {
        return ERROR;
    }
    for (int i = 0; i < len; ++i)
    {
        if ((password[i] ^ 0x42) != ref[i])
        {
            return ERROR;
        }
    }
    printf("Congratulations, you can validate with:\n");
    printf("Flag{%s}\n", password);
    return SUCCESS; 
}

// Password: x0r_m3_f0r_7h3_w1n 
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
