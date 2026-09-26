import os
import sqlite3
import hashlib
import sys
from generate import generer_csv 
from chargement import charger
from traitement import (somme_par_iban_origine,somme_par_banque,somme_par_iban_destinataire,
)
from inserer import inserer_fichier

def calculer_hash(filename: str) -> str:
    h = hashlib.sha256()
    with open(filename, "rb") as fichier:
        for bloc in iter(lambda: fichier.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()
def traiter_fichier(filename: str, db_path: str) -> bool:
    hash_fichier = calculer_hash(filename)
    transactions = charger(filename)

    resultats = {
        "somme_par_iban_origine": somme_par_iban_origine(transactions),
        "somme_par_banque": somme_par_banque(transactions),
        "somme_par_iban_destinataire": somme_par_iban_destinataire(
            transactions
        ),
    }

    return inserer_fichier(
        db_path,
        os.path.basename(filename),
        hash_fichier,
        transactions,
        resultats,
    )


def pipeline(dossier: str = ".", db_path: str = "transactions.db",generer: bool = True) -> int:
    try:
        os.makedirs(dossier, exist_ok=True)
        if generer:
            generer_csv(dossier)
        
    except Exception as e:
        print(f"fail generation : {e}")
        return 1

    fichiers = []
    for nom in sorted(os.listdir(dossier)):
        if nom.endswith(".csv"):
            fichiers.append(os.path.join(dossier, nom))

    echecs = 0
    for filename in fichiers:
        try:
            if traiter_fichier(filename, db_path):
                print(f"ok      {filename}")
            else:
                print(f"ignore  {filename} (contenu deja traite)")
        except Exception as e:
            print(f"fail   {filename} : {e}")
            echecs += 1

    print(f"{echecs} echec(s)")
    return 1 if echecs else 0


if __name__ == "__main__":
     sys.exit(pipeline())