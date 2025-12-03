#!/usr/bin/env python3
from typing import Dict
import sys
import os
import json


def load_dico(dico_file: str) -> Dict[str, str]:
    """Load JSON dictionary from file, return empty dict on missing/invalid file."""
    if not os.path.exists(dico_file):
        return {}
    with open(dico_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            # Ensure the loaded object is a dict; otherwise return empty dict
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            return {}


def save_dico(dico_file: str, dico: Dict[str, str]) -> None:
    with open(dico_file, 'w', encoding='utf-8') as f:
        json.dump(dico, f, ensure_ascii=False, indent=2)


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: dico_local.py <dico_file> <command>")
        print("Commands:")
        print("get <key> : Récupère la valeur associée à la clé. Affiche 'Key not found' si la clé n'existe pas.")
        print("set <key> <value> : Définit la valeur associée à la clé.")
        print("del <key> : Supprime la clé du dictionnaire. Affiche 'Key not found' si la clé n'existe pas.")
        print("pref <prefix> : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.")
        sys.exit(1)

    dico_file: str = sys.argv[1]
    command: str = sys.argv[2]
    dico: Dict[str, str] = load_dico(dico_file)

    if command == 'get':
        if len(sys.argv) != 4:
            print("Usage: dico_local.py <dico_file> get <key>")
            sys.exit(1)
        key: str = sys.argv[3]
        if key in dico:
            print(dico[key])
        else:
            print("Key not found")

    elif command == 'set':
        if len(sys.argv) != 5:
            print("Usage: dico_local.py <dico_file> set <key> <value>")
            sys.exit(1)
        key = sys.argv[3]
        value = sys.argv[4]
        dico[key] = value
        save_dico(dico_file, dico)
        print(f"Set {key} = {value}")

    elif command == 'del':
        if len(sys.argv) != 4:
            print("Usage: dico_local.py <dico_file> del <key>")
            sys.exit(1)
        key = sys.argv[3]
        if key in dico:
            del dico[key]
            save_dico(dico_file, dico)
            print(f"Deleted {key}")
        else:
            print("Key not found")

    elif command == 'pref':
        if len(sys.argv) != 4:
            print("Usage: dico_local.py <dico_file> pref <prefix>")
            sys.exit(1)
        prefix: str = sys.argv[3]
        found: bool = False
        for k, v in dico.items():
            if k.startswith(prefix):
                print(f"{k}: {v}")
                found = True
        if not found:
            print("No keys found with given prefix")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
