## Hardware challenge - First part

### Catégorie 

Hardware 

### Points 

1000

### Format du flag 

Flag{...}

### Description 

Ô noble seigneur, en votre quête, vous avez saisi un artefact insolite, 
propriété de l'adversaire, renfermant des savoirs de grande valeur. 
Hélas, le labeur de déchiffrer ces secrets en leur entièreté vous a échappé. 
Je vous implore, plongez dans les abysses du binaire que vous 
avez arraché des griffes de l'obscurité; au sein de ce labyrinthe numérique, 
il se pourrait bien que vous dénichiez la clé, un indice 
cryptique peut-être, qui éclairera votre chemin vers la maîtrise de cet
engin mystérieux.


### Writeup

The first part of this challenge consists of finding default credentials from 
a partial dump of a fake firmware in order to log into the real device.

The corrupted firmware is `corrupted.bin`. The first thing to do is to identify 
the type of file. One can use either `binwalk`, `unblob` or even `file` which
returns:

``` bash 
file corrupted.bin
corrupted.bin: ARM Cortex-M firmware, initial SP at 0x20007bc0, reset at 0x00014544, 
NMI at 0x00021f0e, HardFault at 0x00014518, SVCall at 0x00014180, PendSV at 0x0001412c
```

Which gives us a crucial piece of information: the architecture. The second thing to 
do is the find the base address, otherwise it will be more difficult to reverse the 
firmware. To do so, one can use `binbloom` like so:

``` bash 
binbloom -t 8 corrupted.bin
[i] File read (158356 bytes)
[i] Endianness is LE
[i] 115 strings indexed
[i] Found 63 base addresses to test
[i] Base address found (valid array): 0x00001000.
 More base addresses to consider (just in case):
  0x1ffdf000 (0.00)
  0x0007b000 (0.00)
  0x27fdf000 (0.00)
```

Now it's possible to load the binary in Ghidra with `0x1000` as base address and 
`Cortex-M` in little endian mode as architecture. The first step in the analysis 
is always to look at the strings, especially the one that visible when connecting
to the chip. By searching for the string `login` we can easily find the login/pwd
to use.

PS: Yes `strings` also work :) 

### Materials

- Some general indications (including a list with tools)

- The log of the boot sequence (can be obtained using `picocom -q --baud 115200 --echo /dev/ttyACM0`):
```
===== Jeanne D'HACK OS is booting =====
Copyright (C) 1412, 1431, 2023, Arc, Inc.
FLASH: 0x00001000-0x00030000
RAM: 0x60000000-0xA0000000
Machine: NRF52840 dongle
Starting system...
Loading Modules...Done
Resetting Configuration...Done
Loading Configuration...Done
done.
System started.
login: test
Password: test
Wrong login or password!
login:
```
- The corrupted dump of the firmware `corrupted.bin`

### Liens utiles 

Liste d'outils:
 - Ghidra
 - arm-none-eabi-objdump
 - xxd 
 - strings 
 - screen
 - picocom
 - pyserial
