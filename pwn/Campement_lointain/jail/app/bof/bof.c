#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define ERROR           -42
#define SUCCESS           0

void show_flag(void) {
  char buffer[64];
  FILE *f = fopen("flag.txt", "rb");
  if (f != NULL) {
    memset(buffer, 0, 64);
    fread(buffer, 64, 1, f);
    printf("%s", buffer);
    fclose(f);
  }
}

int greet(void) {
  char buffer[10];
  memset(buffer, 0, 10);
  printf("Hi! How are you?\n> ");
  if (scanf("%s", buffer) != 1) {
    return ERROR;
  }
  return SUCCESS;
}

int main(int argc, char *argv[]) {
  setvbuf(stdout, NULL, 2, 0);
  printf("greet at %p\n", greet);
  greet();
  printf("I didn't understand...\n");
}
