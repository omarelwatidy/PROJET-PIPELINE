import os
import sqlite3
import tempfile
from chargement import charger
from traitement import (
    somme_par_iban_origine,
    depasse_5000,
)
from test_etape4 import pipeline

def test_pipeline_integration():
    dossier_tmp = tempfile.mkdtemp()
   
    dossier = os.path.join(dossier_tmp, ".")
    db_path = os.path.join(dossier_tmp, "transactions.db")

    code = pipeline(dossier,db_path)
    assert code == 0
    files = [os.path.join(dossier, nom) for nom in sorted(os.listdir(dossier)) if nom.endswith(".csv")]
    assert len(files) > 0
    transactions = []
    for file in files:
        transactions.extend(charger(file))
    total = len(transactions)
    sommes_attendues = somme_par_iban_origine(transactions)
    nb_audessus_5000_attendu = sum(1 for t in transactions if depasse_5000(t))

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM transactions")
    total_database = cur.fetchone()[0]
    assert total_database == total 

    cur.execute("""SELECT iban_origine, SUM(CAST(montant AS REAL)) FROM transactions GROUP BY iban_origine""")
    sommes_database = {iban: montant for iban, montant in cur.fetchall()}

    assert set(sommes_database.keys()) == set(sommes_attendues.keys())

    for iban, montant_attendu in sommes_attendues.items():
        assert round(sommes_database[iban], 2) == round(float(montant_attendu), 2)

    cur.execute("SELECT COUNT(*) FROM transactions WHERE CAST(montant AS REAL) > 5000")
    nb_audessus_5000_database = cur.fetchone()[0]
    assert nb_audessus_5000_database == nb_audessus_5000_attendu
    conn.close()

    code2 = pipeline(dossier, db_path,False)
    assert code2 == 0

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM transactions")
    total_apres_relance = cur.fetchone()[0]
    assert total_apres_relance == total

    cur.execute("SELECT COUNT(*) FROM fichiers_traites")
    nb_fichiers_traites = cur.fetchone()[0]
    assert nb_fichiers_traites == len(files)

    conn.close() 
if __name__ == "__main__":
    test_pipeline_integration()