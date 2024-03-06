#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define ERROR           -42
#define SUCCESS           0
#define BUFFER_SIZE      64

void one_time_pad(char *s1, char *s2) {
  while (*s1 != 0 && *s2 != 0) {
    *s1 = *s1 ^ *s2;
    ++s1;
    ++s2;
  }
}

void read_flag(char *key) {
  char buffer[64];
  FILE *f = fopen("flag.txt", "rb");
  if (f != NULL) {
    memset(buffer, 0, 64);
    fread(buffer, 64, 1, f);
    one_time_pad(buffer, key);
    printf("%s\n", buffer);
    fclose(f);
  } else {
    printf("Fail to open flag file\n");
  }
}

void read_key(char *buffer) {
  FILE *f = fopen("key.txt", "rb");
  if (f != NULL) {
    memset(buffer, 0, 64);
    fread(buffer, 64, 1, f);
    fclose(f);
  } else {
    printf("Fail to open key file\n");
  }
}

int main(int argc, char *argv[]) {
  char buffer[BUFFER_SIZE];
  // Remove stdout buffering
  setvbuf(stdout, NULL, 2, 0);
  printf("Please enter your passphrase: ");
  fgets(buffer, BUFFER_SIZE - 1, stdin);
  // Read the random key
  char key[64];
  read_key(key);
  printf("You entered the following passphrase\n");
  // Format string vulnerability that allow to dump the key
  printf(buffer);
  printf("\nEncrypted flag:\n");
  // Read the key
  read_flag(key);
  printf("Bye!\n\n");
  return SUCCESS;
}
