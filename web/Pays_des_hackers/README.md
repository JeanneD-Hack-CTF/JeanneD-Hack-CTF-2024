## Pays des hackers

### Catégorie

Web

### Poqints

1000

### Format du flag

FLAG_{this_is_a_flag}

### Description

Des murmures dans les tavernes virtuelles et les places de marché numériques évoquaient un territoire truffé de pièges, où seuls les plus habiles pouvaient espérer triompher.

### Writeup

Le site web proposait un formulaire de connexion et d'enregistrement. Lorsqu'on s'enregistre on peut voir que le rôle `Hunter` est aussi envoyé.

En fouillant un peu plus on peut trouver le endpoint `/role` qui renvoie la liste des rôles existants, notamment `Administratorz_du_76`.

Il faut donc se créer en compte en modifiant le rôle dans la requête par celui d'un administrateur. On peut ensuite s'authentifier et on obtient le flag.

En attente du writeup complet.
