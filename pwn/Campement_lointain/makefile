TARGET=bof
CC=gcc
CFLAGS=-Wall -Werror -O0 -m32 -fno-stack-protector -fPIC -pie 
LDFLAGS=

all:
	@$(CC) $(CFLAGS) $(TARGET).c -o $(TARGET) $(LDFLAGS)

clean:
	rm -rf $(TARGET)		
