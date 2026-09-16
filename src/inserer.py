import sqlite3
from typess import Transaction
from decimal import Decimal
#conn = sqlite3.connect("essai.db")
def inserer_fichier(db_path: str,fichier: str,transactions: list[Transaction],resultats: dict[str, dict[str, Decimal]],) -> None:
    with sqlite3.connect(db_path) as conn:
        try:
            cur = conn.cursor()
            cur.executescript("""
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
            fichier_source TEXT NOT NULL
            
        );CREATE TABLE IF NOT EXISTS resultats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fichier_source TEXT NOT NULL,
            traitement TEXT NOT NULL,
            cle TEXT NOT NULL,
            valeur TEXT NOT NULL,
            UNIQUE(fichier_source, traitement, cle)
        );""")
            for t in transactions:
                cur.execute(
                """
                INSERT INTO transactions (
                    datetime_transaction, iban_origine, pays_source,
                    banque_source, iban_destinataire, pays_destinataire,
                    montant, devise, fichier_source
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
                    fichier,
                ),
            )

            for traitement, valeurs in resultats.items():
                for cle, valeur in valeurs.items():
                    cur.execute(
                        """
                        INSERT INTO resultats (fichier_source, traitement, cle, valeur)
                        VALUES (?, ?, ?, ?)
                        """,
                        (fichier, traitement, cle, str(valeur)),
                    )



            conn.commit()
        except Exception: 
            conn.rollback() 
            raise
  