#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define ERROR           -42
#define SUCCESS           0

#define NAME_SIZE        32
#define TEACHER          42 
#define STUDENT           0
#define BUFFER_SIZE     512

typedef struct user {
  int type;
  char name[NAME_SIZE];
} user;

typedef struct subject {
  char name[NAME_SIZE];
  int coef;
} subject; 

void *create_user(int type, char *name) {
  if (type == TEACHER) {
    return NULL;
  }
  user *u = malloc(sizeof(user));
  if (u != NULL) {
    strncpy(u->name, name, NAME_SIZE - 1);
    u->name[NAME_SIZE] = 0;
    u->type = STUDENT;
  }
  return u;
}

void get_flag(user *u) {
  size_t count = 0;
  char buffer[BUFFER_SIZE];
  if (u && u->type == TEACHER) {
    FILE *f = fopen("/app/uaf/flag.txt", "r");
    if (f != NULL) {
      fgets(buffer, BUFFER_SIZE, f);
      fclose(f);

      printf("Hello Teacher, Here is the flag:\n%s\n", buffer);
    }
  } else {
    printf("Student are not authorized to read flags!\n");
  }
}
void delete_user(user *u) {
  free(u);
  u = NULL;
} 

void *create_subject(char *name) {
  subject *s = malloc(sizeof(subject));
  if (s != NULL) {
    strncpy(s->name, name, NAME_SIZE - 1);
    s->name[NAME_SIZE] = 0;
    s->coef = random() % 10;
  }
  return s; 
}

void delete_subject(subject *s) {
  free(s);
  s = NULL;
}

int main(int argc, char *argv[]) {
  int choice = 0;
  user *u = NULL;
  subject *s = NULL; 
  char buffer[BUFFER_SIZE];
  ssize_t count = 0;

  // Disable buffering
  setvbuf(stdout, NULL, 2, 0);     
  // Init random
  srandom(time(NULL));
  printf("Welcome to ADE 2.0\n");

  while (1) {
    printf("Menu:\n");
    printf("1. Create user\n");
    printf("2. Create subject\n");
    printf("3. Read Flag\n");
    printf("4. Delete user\n");
    printf("5. Delete subject\n");
    printf("6. Close ADE\n");
    printf(">>> ");
    fflush(stdout);
    if (scanf("%d", &choice) != 1) {
      exit(ERROR);
    }
    switch (choice) {
      case 1:
        if (u == NULL) {
          printf("Username: ");
          memset(buffer, 0, BUFFER_SIZE);
          count = read(0, buffer, BUFFER_SIZE);
          if (count <= 0) {
            exit(ERROR);
          } 
          // Remove trailing newline
          buffer[count > 0 ? count - 1 : 0] = 0;
          u = create_user(STUDENT, buffer);
        } else {
          printf("Cannot create more than one user, sorry :/\n");
        }
        break;
      case 2:
        if (s == NULL) {
          printf("Subject name: ");
          memset(buffer, 0, BUFFER_SIZE);
          count = read(0, buffer, BUFFER_SIZE);
          if (count <= 0) {
            exit(ERROR);
          } 
          // Remove trailing newline
          buffer[count > 0 ? count - 1 : 0] = 0;
          s = create_subject(buffer);
        } else {
          printf("Cannot create more than one subject, sorry ADE is still in beta\n");
        }
        break;
      case 3:
        get_flag(u);
        break;
      case 4:
        delete_user(u);
        break;
      case 5:
        delete_subject(s);
      case 6:
        /* fallthrough */
      default:
        exit(SUCCESS);
    }
  }
  return SUCCESS;
}
