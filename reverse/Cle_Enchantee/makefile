TARGET=keygen
CC=gcc
CFLAGS=-Wall
LDFLAGS=

all:
	$(CC) $(CFLAGS) $(TARGET).c -o $(TARGET) $(LDFLAGS)
	strip $(TARGET)

clean:
	rm -rf $(TARGET)		
