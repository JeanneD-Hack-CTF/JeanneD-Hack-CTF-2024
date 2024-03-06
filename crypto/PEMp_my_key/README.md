## PEMp my key !

### Catégorie

Crypto

### Points

1000

### Format du flag

Créer un clé privée RSA valide au format PEM contenant le motif 
suivant : `/jeannedhackctf/`.

### Description

Je fais partie de ces aventuriers toujours en quête de moyens de communication 
singuliers. Et si nous passions par des clés RSA pour échanger nos messages ? 

Imaginez-vous, nous pourrions transmettre nos secrets les plus précieux en les 
enveloppant dans des clés cryptographiques. Essayons quelque chose d'unique: 
envoyez-moi une clé privée RSA valide au format PEM, ornée du motif suivant:
`/jeannedhackctf/`

#### Précisions

La clé RSA doit contenir le motif demandé. Il doit être obtenu directement en 
générant une clé RSA, en essayant de modifier les paramètres de la clé sur 
lesquels vous avez la main. Le motif ne doit pas être ajouté à la main après 
la génération de la clé.

### Détails

Le fichier `check.sh` fourni permet de vérifier que votre clé privée est valide 
avant de la soumettre au serveur. Une clé valide doit retourner la sortie
suivante:
```bash
> ./check.sh key.pem
[+] Key contains pattern
[+] RSA key ok
```

Une fois la clé privée validée de votre côté, connectez vous au serveur et 
soumettez votre clé pour récupérer le flag.
```
nc <IP_HOST> 50002
```

**Attention** : cela ne sert à rien de tester toutes vos clés avec le serveur, 
il lancera exactement le même script de vérification que celui fourni ! Et 
donc pour limiter le nombre de requêtes, vérifier d'abord en local !
