# Projet Dictionnaire avec Python socket

## 1. But

Fournir une application client/serveur en Python avec un client dico_client.py et un serveur dico_server.py qui permettent de manipuler à distance un dictionnaire en utilisant des sockets TCP. Les échanges se font sur une connexion TCP, en texte brut (UTF-8), suivant une structure ligne par ligne. Chaque message correspond à une requête ou une réponse terminée par le caractère “\n”.

## 2. Structure des Messages

Terminaison de Ligne : Chaque ligne de commande est strictement terminée par **CRLF** (\r\n).
Séparateur : L'**espace** est utilisé comme séparateur entre les éléments de la ligne de commande.

## 3. Format de la commande de connexion

Exemples de requêtes en fonction des différentes commandes disponibles

**Commande de connexion pour le Client :**

`./dico_client.py <@serveur> <port du serveur> <dico_name.json> <commande>`

**Commande de connexion pour le Client Administrateur :**

- Particularité pour l’admin, le client administrateur devra s'authentifier auprès du serveur :

`./dico_admin.py <@serveur> <port du serveur>`

- De plus, il pourra rester connecté pour effectuer plusieurs opérations du type :

`<dico_name.json> <commande>`  
`<dico_name.json> <commande>`  
`…`
- Pour fermer la connexion avec l’admin, il faut alors un moyen de reconnaître la demande du client admin avec une commande spéciale :  
`exit`

**Commande de démarrage du Serveur :**

`./dico_server.py <port d'écoute> [master <@serveur maître> <port du serveur maître>]`

### Liste des différentes commandes :

**Commandes pour le Client Non Administrateur :**

`get` &lt;clé&gt; : Récupère la valeur associée à la clé. 

`pref` &lt;préfixe&gt; : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.

**Commandes pour le Client Administrateur :**

`get` &lt;clé&gt; : Récupère la valeur associée à la clé. 

`pref` &lt;préfixe&gt; : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.

`set` &lt;clé&gt; &lt;valeur&gt; : Définit la valeur associée à la clé ou crée la clé et rempli avec la valeur

`del` &lt;clé&gt; : Supprime la clé du dictionnaire. 

## 4. Format de la réponse :

Exemples de réponses en fonction des différentes commandes disponibles  
*{utilisateur} est soit client soit administrateur.*

**Serveur Maître**
Si un serveur maître est défini dans la requête et si le serveur esclave ne trouve pas de réponse alors le serveur maître répond à la requête de la même manière que ci dessous. Si il ne trouve quand même pas il renverra la même erreur que ci dessous.
Le serveur Maître répond de la même manière que le serveur Esclave faux ou non.

**Retours Sans Erreur :**

`get` : renvoie la valeur associé à la clef

*Exemple* : `./dico_{utilisateur}.py 10.0.104.4 7777 mois_duree.json get avril` -> 30

`set` : renvoie rien, modifie seulement la valeur de la clé ou ajoute la clé et la valeur associée

`del` : renvoie rien, supprime seulement la clé et la valeur associée

`pref` : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.

*Exemple* : `./dico_{utilisateur}.py 10.0.104.4 7777 mois_duree.json pref ju` -> "juin": "30" "juillet": "31"

**Erreur dans les commandes au niveau des arguments:**

`get` Si la clé n'existe pas :  
Key not found  

*Exemple* : `./dico_{utilisateur}.py 10.0.104.4 7777 mois_duree.json get tutu`
où “tutu” n’est pas une clé existante

`set` :  
Pas d’erreur possible

`del` Si la clé n'existe pas :  
Key not found  

*Exemple* : `./dico_{utilisateur}.py 10.0.104.4 7777 mois_duree.json del tutu`
où “tutu” n’est pas une clé existante

`pref` Si le préfixe n’est associé à aucune clé :  
Prefix not found  

*Exemple 1* : `./dico_{utilisateur}.py 10.0.104.4 7777 mois_duree.json pref tutu`
ou "tutu" n’est pas un préfixe existant

*Exemple 2* : `./dico_{utilisateur}.py 10.0.104.4 7777 mois_duree.json pref féb`
féb n’est pas un préfixe existant, c’est fév. qui est un des préfixes existant pour février.

**Erreurs sur le nom des commandes et du nombre d’arguments :**

**Pour un client non administrateur :**

Si la commande à moins de 1 argument ou n’existe pas :  
Usage: dico_client.py &lt;server&gt; &lt;port&gt; &lt;command&gt; &lt;arg&gt;  

*Exemple 1* : `./dico_client.py 10.0.104.4 7777 mois_duree.json get`
où il manque un argument

*Exemple 2* : `./dico_client.py 10.0.104.4 7777 mois_duree.json toto`
où "toto" n’est pas une commande existante

Si la commande est `set` ou `del` :  
VOUS DEVEZ ÊTRE ADMIN  

Si la commande n'existe pas et a plus d’un argument :  
Usage: dico_client.py &lt;server&gt; &lt;port&gt; &lt;dico_name.json&gt; &lt;command&gt; &lt;arg&gt;  
Commands:  
get &lt;key&gt; : Récupère la valeur associée à la clé. Affiche 'Key not found' si la clé n'existe pas.  
pref &lt;prefix&gt; : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.  

*Exemple* : `./dico_client.py 10.0.104.4 7777 mois_duree.json toto tutu` 
où "toto" n’est pas une commande existante

**Pour un client administrateur :**

Si la commande à moins de 1 argument ou n’existe pas :  
Usage: dico_admin.py &lt;server&gt; &lt;port&gt; &lt;command&gt; &lt;arg&gt;  

*Exemple 1* : `./dico_admin.py 10.0.104.4 7777 mois_duree.json get`
où il manque un argument

*Exemple 2* : `./dico_admin.py 10.0.104.4 7777 mois_duree.json toto`
où "toto" n’est pas une commande existante

Si la commande est set et il manque le deuxième argument :  
Usage: dico_admin.py &lt;server&gt; &lt;port&gt; &lt;command&gt; &lt;arg&gt; &lt;arg2&gt;  

*Exemple* : `./dico_admin.py 10.0.104.4 7777 mois_duree.json set avril`
où il manque un argument

Si la commande n'existe pas et a plus d’un argument :  
Usage: dico_admin.py &lt;server&gt; &lt;port&gt; &lt;dico_name.json&gt; &lt;command&gt; &lt;arg&gt;  
Commands:  
get &lt;key&gt; : Récupère la valeur associée à la clé. Affiche 'Key not found' si la clé n'existe pas.  
pref &lt;prefix&gt; : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.  
set &lt;key&gt; &lt;value&gt; : Définit la valeur associée à la clé ou crée la clé et rempli avec la valeur  
del &lt;key&gt; : Supprime la clé du dictionnaire.  
  
*Exemple* : `./dico_admin.py 10.0.104.4 7777 mois_duree.json toto tutu` 
où "toto" n’est pas une commande existante

## 5. Protocoles des fonctionnalités

- le client a besoin du host + port + dico + cmd + arg, -> se connecte avec l'adresse de la machine host, le port reçu du serveur
- le serveur a besoin du port -> demarre le serv