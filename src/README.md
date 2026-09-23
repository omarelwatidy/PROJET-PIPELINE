

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

## lignes invalides

`charger()` valide l'en-tête du CSV et lève une exception si les colonnes
ne correspondent pas au format attendu. Une ligne avec un montant non
numérique leve une exception jusqu'à
le pipeline, qui marque ce fichier `fail` et continue avec les suivants
(voir étape 6). Aucune ligne partielle d'un fichier en échec n'est insérée :
l'insertion d'un fichier se fait dans une seule transaction Sqlite, et 
c'est annulé  en cas d'erreur.

## idempotence

Chaque fichier est identifié par le hash de son contenu, donc deux noms différents pour un même contenu donnent le même hash et le fichier est traité une fois, un même nom réutilisé pour un contenu différent est traité comme un nouveau fichier. Le hash est inséré dans fichiers_traites (colonne UNIQUE) dans la même transaction que les lignes de transactions et resultats, donc soit tout est inséré, soit
rien n'est insérer.

## Étape 6 - comportement en cas d'échec

Sortie de la pipeline avec un fichier dont un montant est non numérique :

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

le fichier en echec n'est pas inserer

Erreur détectée par mypy et non par les tests :

def formatter_montant(transaction: Transaction) -> str:
    return "Montant: " + transaction["montant"]



j'ai ecrit une fonction qui n'est pas utilisé qui concatene un str et un decimal.J'ai eu cette erreur:

mypy traitement.py
traitement.py:45: error: Unsupported operand types for + ("str" and "Decimal")  [operator]
Found 1 error in 1 file (checked 1 source file)
Cela montre que les tests ne couvrent que le code exécuté, alors que mypy
vérifie la cohérence des types indépendamment de l'exécution.Donc les deux
outils sont complémentaires, pas substituables.



## Étape 7 - retry
Pour sqlite3.OperationalError, c'est quand  un autre
processus a une transaction d'écriture ouverte sur le même fichier
au même instant. Ce n'est pas une erreur sur les données ni sur la requête
si on réessaie quelques millisecondes plus tard, la même insertion, avec les
mêmes valeurs, a de bonnes chances de réussir, car l'état qui bloquait
l'opération a disparu entre-temps. Donc on peut utiliser retry dans ce cas.

Pour sqlite3.IntegrityError, c'est à cause d'une contrainte violée (UNIQUE, NOT NULL, FOREIGN KEY). Si l'insertion d'un hash déjà présent échoue à cause de la contrainte
UNIQUE, réessayer la même insertion échouera chaque fois exactement de la même façon,donc on doit pas utliser un retry . 




