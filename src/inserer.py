import sqlite3
from typess import Transaction
from decimal import Decimal
#conn = sqlite3.connect("essai.db")
def inserer_fichier(db_path: str,fichier: str,hash_fichier: str,transactions: list[Transaction],resultats: dict[str, dict[str, Decimal]],) -> bool:
    with sqlite3.connect(db_path) as conn:
        try:
            cur = conn.cursor()
            cur.executescript("""
            CREATE TABLE IF NOT EXISTS fichiers_traites (
            hash_fichier TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            date_traitement TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime_transaction TEXT NOT NULL,
            iban_origine TEXT NOT NULL,
            pays_source TEXT NOT NULL,
            banque_source TEXT NOT NULL,
            iban_destinataire TEXT NOT NULL,
            pays_destinataire TEXT NOT NULL,
            montant TEXT NOT NULL,
            devise TEXT NOT NULL,
            hash_fichier TEXT NOT NULL REFERENCES fichiers_traites(hash_fichier)
        );CREATE TABLE IF NOT EXISTS resultats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash_fichier TEXT NOT NULL REFERENCES fichiers_traites(hash_fichier),
            traitement TEXT NOT NULL,
            cle TEXT NOT NULL,
            valeur TEXT NOT NULL,
            UNIQUE(hash_fichier, traitement, cle)
        );""")
            try:
                cur.execute(
                    "INSERT INTO fichiers_traites (hash_fichier, nom) VALUES (?, ?)",
                    (hash_fichier, fichier),
                )
            except Exception:
                return False
                
            for t in transactions:
                cur.execute(
                """
                INSERT INTO transactions (
                        datetime_transaction, iban_origine, pays_source,
                        banque_source, iban_destinataire, pays_destinataire,
                        montant, devise, hash_fichier
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                        t["datetime_transaction"].isoformat(),
                        t["iban_origine"],
                        t["pays_source"],
                        t["banque_source"],
                        t["iban_destinataire"],
                        t["pays_destinataire"],
                        str(t["montant"]),
                        t["devise"],
                        hash_fichier,
                    ),
            )

            for traitement, valeurs in resultats.items():
                for cle, valeur in valeurs.items():
                    cur.execute(
                        """
                        INSERT INTO resultats (hash_fichier, traitement, cle, valeur)
                        VALUES (?, ?, ?, ?)
                        """,
                        (hash_fichier, traitement, cle, str(valeur)),
                    )



            conn.commit()
            return True             
        except Exception: 
            conn.rollback() 
            raise
  