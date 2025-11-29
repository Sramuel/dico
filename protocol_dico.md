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
* **SET** : `<dico> set <clé> <valeur>`
* **DEL** : `<dico> del <clé>`


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
| `Error: Invalid request format` | Le message reçu est malformé (il manque des espaces ou des arguments). |
| `Unknown command: <cmd>` | La commande demandée (ex: "toto") n'existe pas. |