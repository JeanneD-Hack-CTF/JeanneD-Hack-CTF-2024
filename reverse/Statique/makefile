TARGET=static
SOLVE=solve
CC=gcc
CFLAGS=-Wall
LDFLAGS=-static

all:
	$(CC) $(CFLAGS) $(TARGET).c -o $(TARGET) $(LDFLAGS)
	$(CC) $(CFLAGS) $(SOLVE).c -o $(SOLVE)
	strip $(TARGET)

clean:
	rm -rf $(TARGET) $(SOLVE)	
