import os
import sqlite3

from chargement import charger
from traitement import (somme_par_iban_origine,somme_par_banque,somme_par_iban_destinataire,
)
from inserer import inserer_fichier

def test_pipeline() -> None:
    transactions = charger("transactions_2026-09-01.csv")
    for transaction in transactions:
        print(transaction)
    
    resultats = {
        "somme_par_iban_origine": somme_par_iban_origine(transactions),
        "somme_par_banque": somme_par_banque(transactions),
        "somme_par_iban_destinataire": somme_par_iban_destinataire(
            transactions
        ),
    }

    inserer_fichier(
        "test.db",
        "transactions_2026-09-01.csv",
        transactions,
        resultats,
    )
if __name__ == "__main__":
    test_pipeline()