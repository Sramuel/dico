# Protocole - Projet Dictionnaire

## 1. Introduction et But

Le but est de faire communiquer un client et un serveur pour consulter un dictionnaire à distance.
Les échanges se font via le réseau en utilisant des **sockets TCP**.
Toutes les données échangées sont du **texte brut**, encodé en **UTF-8**.

Il y a deux types d'échanges principaux :
1. **Client -> Serveur** : Le client pose une question.
2. **Serveur -> Serveur Maître** : Si le serveur ne sait pas, il transfère la question à son chef (le maître).


## 2. Structure des Messages (Le Protocole)

C'est la règle pour que le client et le serveur se comprennent.
On n'utilise pas de JSON complexe, mais une structure simple ligne par ligne.

### Format de la requête (Ce qu'envoie le client)
Le client envoie une chaîne de caractères composée de 3 parties, séparées obligatoirement par un **espace**.

**Syntaxe :**
`NOM_DU_DICO` `COMMANDE` `ARGUMENT`

* **Séparateur** : Espace (` `).
* **Encodage** : UTF-8.

**Exemple concret (ce qui circule dans le réseau) :**
`mois_duree.json get avril`

### Format de la réponse (Ce que répond le serveur)
Le serveur renvoie directement le résultat sous forme de texte brut.


## 3. Détail des Commandes

Exemples de requêtes en fonction des différentes commandes disponibles

**Requête pour le Client :**

`./dico_client.py <@serveur> <port du serveur> <dico_name.json> <commande>`

**Requête pour le Client Administrateur :**

- Particularité pour l’admin, le client administrateur devra s'authentifier auprès du serveur :

`./dico_admin.py <@serveur> <port du serveur> <username> <password>`

- De plus, il pourra rester connecté pour effectuer plusieurs opérations du type :

`<dico_name.json> <commande>`  
`<dico_name.json> <commande>`  
`…`
- Pour fermer la connexion avec l’admin, il faut alors un moyen de reconnaître la demande du client admin avec une commande spéciale :  
`exit`

**Requête pour le Serveur :**

`./dico_server.py <port d'écoute> [master <@serveur maître> <port du serveur maître>]`

Voici les interactions possibles définies dans le protocole.

### Commande GET
* **But** : Demander la valeur exacte d'une clé.
* **Format envoyé** : `<dico> get <clé>`
* **Réponse succès** : La valeur associée (ex: `30`).
* **Réponse erreur** : `Key not found`

**Exemple d'échange :**
> **Envoi** : `mois_duree.json get avril`
> **Réception** : `30`

### Commande PREF
* **But** : Demander toutes les clés qui commencent par un préfixe.
* **Format envoyé** : `<dico> pref <préfixe>`
* **Réponse succès** : Une liste de couples formatée : `"clé": "valeur" "clé2": "valeur2"`
* **Réponse erreur** : `Prefix not found`

**Exemple d'échange :**
> **Envoi** : `mois_duree.json pref ju`
> **Réception** : `"juin": "30" "juillet": "31"`

### Commandes Administrateur (SET / DEL)
*Ces commandes sont réservées aux administrateurs.*

### Commande SET
* **But** : Ajouter une nouvelle entrée ou modifier une entrée existante dans le dictionnaire.
* **Format envoyé** : `<dico> set <clé>|<valeur>`
    * *Note : La clé et la valeur doivent être séparées par un caractère pipe (`|`) sans espaces autour.*
* **Réponse succès** : `Set <clé> = <valeur>`
* **Réponse erreur** : `Error in set arguments` (si le format `clé|valeur` n'est pas respecté).

**Exemple d'échange :**
> **Envoi** : `mois_duree.json set thermidor|30`
> **Réception** : `Set thermidor = 30`

### Commande DEL
* **But** : Supprimer une entrée du dictionnaire.
* **Format envoyé** : `<dico> del <clé>`
* **Réponse succès** : `Deleted <clé>`
* **Réponse erreur** : `Key not found`

**Exemple d'échange :**
> **Envoi** : `mois_duree.json del juillet`
> **Réception** : `Deleted juillet`


## USAGE

* **Préparation** : Faire `/sbin/ifconfig` et remplacer les `@host` par les IP (Ctrl+H dans VS Code).

### 1\. Test Maître / Esclave

**Sur le HOST 1 (Maître)**

```bash
cd ~/dico-A5-05/tests/serveur_maitre/
./dico_server.py 7777
```

**Sur le HOST 2 (Esclave)**

```bash
cd ~/dico-A5-05/tests/serveur_esclave/
./dico_server.py 8888 master @host1 7777
```

**Sur le HOST 3 (Client)**

```bash
cd ~/dico-A5-05/
./dico_client.py @host2 8888 punchlines.json get Bruce Lee
./dico_client.py @host2 8888 punchlines.json pref A
./dico_client.py @host2 8888 mois_duree.json get juin
./dico_client.py @host2 8888 mois_duree.json pref j
```

-----

### 2\. Test Dico Admin

**Sur le HOST 1 (Serveur)**

```bash
cd ~/dico-A5-05/
./dico_server.py 7777
```

**Sur le HOST 2 (Admin - Connexion)**

```bash
./dico_admin.py @host1 7777 demo-user demo-password
./dico_admin.py @host1 7777 admin a
./dico_admin.py @host1 7777 admin admin
```

**Une fois connecté (commandes internes)**

```text
mois_duree.json set juin|20
mois_duree.json del juin
punchlines.json del Bruce Lee
punchlines.json set John F. Kennedy|La victoire a cent pères, mais la défaite est orpheline.
exit
```

```bash
./dico_client.py @host1 7777 punchlines.json get John F. Kennedy
./dico_client.py @host1 7777 punchlines.json pref J
```


## 4. Fonctionnement Serveur Maître / Esclave

Le protocole gère une hiérarchie pour trouver l'information coûte que coûte.

1.  Le **Serveur Esclave** reçoit une requête (ex: `get février`).
2.  Il cherche dans son fichier local.
3.  **Si il ne trouve pas** (ou si le fichier n'existe pas) ET qu'il a un maître configuré :
    * Il ouvre une connexion vers le Serveur Maître.
    * Il lui envoie le message **tel quel** (sans le modifier).
    * Il attend la réponse du Maître.
    * Il renvoie cette réponse au client.

C'est transparent pour le client : il ne sait pas que c'est le maître qui a répondu.


## 5. Gestion des Erreurs

Le serveur renvoie des messages précis en texte clair pour dire ce qui ne va pas.

| Message renvoyé | Signification |
| :--- | :--- |
| `Key not found` | La clé n'existe pas (ni chez l'esclave, ni chez le maître). |
| `Prefix not found` | Aucun mot ne commence par ce préfixe. |
| `Malformed request` | Le message reçu est malformé (il manque des espaces ou des arguments). |
| `Unknown command: <cmd>` | La commande demandée (ex: "toto") n'existe pas. |