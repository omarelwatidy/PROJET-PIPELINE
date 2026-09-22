python test_integration.py
fail   ./transactions_2026-09-01.csv : [<class 'decimal.ConversionSyntax'>]
ignore  ./transactions_2026-09-09.csv (contenu deja traite)
ignore  ./transactions_2026-09-10.csv (contenu deja traite)
1 echec(s)
Traceback (most recent call last):
  File "/Users/omarelwatidy/projet-pipeline/src/test_integration.py", line 58, in <module>
    test_pipeline_integration(".","transactions.db")
  File "/Users/omarelwatidy/projet-pipeline/src/test_integration.py", line 14, in test_pipeline_integration
    assert code == 0
           ^^^^^^^^^
AssertionError

mypy traitement.py
traitement.py:45: error: Unsupported operand types for + ("str" and "Decimal")  [operator]
Found 1 error in 1 file (checked 1 source file)
def formatter_montant(transaction: Transaction) -> str:
    return "Montant: " + transaction["montant"]

# Pipeline 

## Installation

    python -m venv venv
    source venv/bin/activate      
    pip install pytest mypy

## Commandes

Lancer le pipeline complet:

    python test_etape3.py

Lancer les tests :

    pytest -v

Vérifier les types :

    mypy .

## Schéma de la base

    fichiers_traites (
        hash_fichier      TEXT PRIMARY KEY, 
        nom               TEXT NOT NULL,
        date_traitement   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )

    transactions (
        id                    INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime_transaction  TEXT NOT NULL,
        iban_origine          TEXT NOT NULL,
        pays_source           TEXT NOT NULL,
        banque_source         TEXT NOT NULL,
        iban_destinataire     TEXT NOT NULL,
        pays_destinataire     TEXT NOT NULL,
        montant               TEXT NOT NULL,   
        devise                TEXT NOT NULL,
        hash_fichier          TEXT NOT NULL REFERENCES fichiers_traites(hash_fichier)
    )

    resultats (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        hash_fichier  TEXT NOT NULL REFERENCES fichiers_traites(hash_fichier),
        traitement    TEXT NOT NULL,
        cle           TEXT NOT NULL,
        valeur        TEXT NOT NULL,
        UNIQUE(hash_fichier, traitement, cle)
    )

