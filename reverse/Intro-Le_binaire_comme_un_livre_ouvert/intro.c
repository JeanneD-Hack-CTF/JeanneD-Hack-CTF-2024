#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ERROR       -42
#define SUCCESS       0
 
int check_password(char *pwd) {
    const char *ref = "J34nn3D'h4ck_CTF_1nTr0"; 
    if (strncmp(pwd, ref, strlen(ref)) == 0) {
        printf("Congratulations, you can validate with:\n");
        printf("Flag{%s}\n", ref);
        return SUCCESS;
    }
    return ERROR;
}

// Password: J34nn3D'h4ck_CTF_1nTr0
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
