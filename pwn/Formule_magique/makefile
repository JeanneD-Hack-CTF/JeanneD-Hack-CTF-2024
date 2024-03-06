TARGET=fmt
CC=gcc
CFLAGS=-O0 -m32 -fno-stack-protector -fPIC -pie 
LDFLAGS=
KEY=key.txt

all: $(TARGET)
	@echo "Done"

$(TARGET): $(KEY)
	@echo "Compiling"
	@$(CC) $(CFLAGS) $(TARGET).c -o $(TARGET) $(LDFLAGS)

$(KEY):
	@echo "Generating new key"
	@dd if=/dev/random bs=1 count=32 2> /dev/null > $@ 

clean:
	rm -rf $(TARGET)	

fullclean:
	rm -rf $(TARGET) $(KEY)	

