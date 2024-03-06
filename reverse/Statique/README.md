## Statique

### Catégorie

Reverse

### Points

1000

### Format du flag 

Flag{this_is_a_flag}

### Description
La clé USB ancienne révélait des secrets du passé. Les érudits se plongeaient 
dans les fichiers comme dans les pages d'un grimoire. Chaque fichier était 
une énigme à résoudre. Ainsi débutait une quête épique, où mystère et 
découverte se mêlaient.

### Writeup

Le but du chall est de bruteforce la clef utilisé pour "chiffrer" le flag, vu 
que l'on sait que le flag commence par `Flag`, il est possible de trouver la 
bonne clef (voir `solve.c`).
