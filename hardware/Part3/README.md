## Hardware challenge - Third part

### Catégorie 

Hardware 

### Points 

1000

### Format du flag 

Flag{...}

### Description 

Nouvelles louanges vous sont dues, preux chevalier, car vous avez triomphé 
de la seconde épreuve, une joute d'astuces loin d'être aisée. Votre périple 
vous mène désormais vers un défi de taille : l'exploitation d'une faille au 
sein d'un protocole éthéré, celui que l'on nomme par le cryptique sobriquet 
de la "dent bleu".

Soyez averti, cette quête ne sera point de tout repos, un véritable tournoi 
de l'esprit et de la ruse vous attend. Armez-vous de courage, car le chemin 
à parcourir est semé d'embûches et de mystères à dévoiler. Puissiez-vous 
trouver la force et la sagacité nécessaires pour surmonter cette épreuve 
avec honneur et vaillance. En avant, que votre quête soit couronnée 
de succès !

### Writeup

The last part is about doing a RCE on the device using BLE. Upon connecting 
to the chip, the following services are enabled:
```
> bluetoothctl
[bluetooth]# scan on
[bluetooth]# devices
Device DB:1D:51:07:F2:0A JeanneD'Hack CTF
...
[bluetooth]# connect DB:1D:51:07:F2:0A
Attempting to connect to DB:1D:51:07:F2:0A
[CHG] Device DB:1D:51:07:F2:0A Connected: yes
Connection successful
[NEW] Primary Service (Handle 0x0000)
	/org/bluez/hci0/dev_DB_1D_51_07_F2_0A/service0001
	00001801-0000-1000-8000-00805f9b34fb
	Generic Attribute Profile
[NEW] Characteristic (Handle 0x0000)
	/org/bluez/hci0/dev_DB_1D_51_07_F2_0A/service0001/char0002
	00002a05-0000-1000-8000-00805f9b34fb
	Service Changed
[NEW] Descriptor (Handle 0x0000)
	/org/bluez/hci0/dev_DB_1D_51_07_F2_0A/service0001/char0002/desc0004
	00002902-0000-1000-8000-00805f9b34fb
	Client Characteristic Configuration
[NEW] Characteristic (Handle 0x0000)
	/org/bluez/hci0/dev_DB_1D_51_07_F2_0A/service0001/char0005
	00002b29-0000-1000-8000-00805f9b34fb
	Client Supported Features
[NEW] Characteristic (Handle 0x0000)
	/org/bluez/hci0/dev_DB_1D_51_07_F2_0A/service0001/char0007
	00002b2a-0000-1000-8000-00805f9b34fb
	Database Hash
[NEW] Primary Service (Handle 0x0000)
	/org/bluez/hci0/dev_DB_1D_51_07_F2_0A/service0010
	28dac133-0bec-589b-234a-c21d8bde9f85
	Vendor specific
[NEW] Characteristic (Handle 0x0000)
	/org/bluez/hci0/dev_DB_1D_51_07_F2_0A/service0010/char0011
	0c169adc-5d11-09a0-974c-17f800a0c19c
	Vendor specific
[NEW] Characteristic (Handle 0x0000)
	/org/bluez/hci0/dev_DB_1D_51_07_F2_0A/service0010/char0013
	0ec46cb2-63c8-3298-ce47-5d57c0570695
	Vendor specific
[CHG] Device DB:1D:51:07:F2:0A ServicesResolved: yes
[JeanneD'Hack CTF]#
```

It's possible to exchange with the device using bluetoothctl (with `gatt` submenu) but it's
not very convenient so one can use `pygatt` to send and write some data. Basically, the 
service `28dac133-0bec-589b-234a-c21d8bde9f85` has two Characteristic, the `0c169adc-5d11-09a0-974c-17f800a0c19c
` allow to write values and the other sends back the data written surrounded by `Flag{...}`.

This service is also vulnerable to buffer overflow, the whole point is to redirect code execution
the function that prints the last flag. Since this part of the challenge is hard, there is a high 
chance that nobody will have the time to do it but in theory it's feasible. 


