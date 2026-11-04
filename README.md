# Projet Dictionnaire

Client et serveur de dictionnaire communiquant par sockets TCP, avec prise en charge d'une architecture maître/esclave et d'un client administrateur.

## Pré-requis

- Python 3
- Deux ou trois machines/terminaux capables de communiquer sur le réseau

## Lancer un serveur

```bash
./dico_server.py 7777
```

Serveur esclave avec un maître :

```bash
./dico_server.py 8888 master <hote-maitre> 7777
```

## Utiliser le client

```bash
./dico_client.py <hote> <port> <dictionnaire.json> get <cle>
./dico_client.py <hote> <port> <dictionnaire.json> pref <prefixe>
```

## Utiliser le client administrateur

Le serveur de démonstration utilise les identifiants de test `admin` / `admin`.

```bash
./dico_admin.py <hote> <port> admin admin
```

Les commandes administrateur sont ensuite saisies sous la forme `fichier.json set cle|valeur` ou `fichier.json del cle`. Tapez `exit` pour quitter.

La description complète du protocole et des scénarios de test se trouve dans [protocol_dico.md](protocol_dico.md).
