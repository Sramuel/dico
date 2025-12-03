#!/usr/bin/env python3

def format_request(dico, command, arg): #prépare le message pour l'envoi (client -> serveur)
    msg = f"{dico} {command} {arg}"
    return msg.encode("utf-8")

def parse_request(data): #découpe le message reçu (serveur <- client)
    try:
        text = data.decode("utf-8").strip()
        parts = text.split(" ", 2) #on divise en 3 parties max (pour gérer les espaces dans l'argument)
        if len(parts) < 3:
            return None
        return parts #retourne [dico, command, arg]
    except:
        return None