## Relatively Secret Agency

### Catégorie

Crypto

### Points

1000

### Format du flag 

FLAG{this_is_a_flag}

### Description

Un mystérieux émissaire a envoyé le même message à trois seigneurs différents, 
cachant chaque message avec le sceau magique de son destinataire. Retrouvez le 
message et vous pourrez obtenir des informations précieuses concernant un drapeau !

### Writeup 

Un challenge de crypto classique, pour mettre en pratique une attaque vu 
théoriquement pendant le cours.

Une personne utilise trois clés publiques différentes pour envoyer le même 
message à ces trois interlocuteurs. Cependant, pour chacune des clés l'exposant 
publique est e = 3, on peut donc utiliser **l'attaque de Hastad** pour calculer 
le clair à partir des 3 chiffrés et des 3 clés publiques.

Fichier attaché : `secret.zip`

- Le fichier `flag.txt` doit faire précisément 512 octets étant donné que RSA 
est utilisé ici sans padding pour que l'attaque fonctionne (d'où le texte, 
merci chatGPT).
