import csv
from datetime import datetime
from decimal import Decimal
from typess import Transaction


def charger(filename: str) -> list[Transaction]:
    transactions = []
    with open(filename, "r") as fichier:
        reader = csv.DictReader(fichier)
        if reader.fieldnames != ["datetime_transaction","iban_origine","pays_source","banque_source","iban_destinataire","pays_destinataire","montant","devise"]:
            raise Exception("invalides")

        for ligne in reader:
            transaction: Transaction = {
                "datetime_transaction": datetime.fromisoformat(
                    ligne["datetime_transaction"]
                ),
                "iban_origine":ligne["iban_origine"],
                "pays_source":ligne["pays_source"],
                "banque_source":ligne["banque_source"],
                "iban_destinataire": ligne["iban_destinataire"],
                "pays_destinataire":ligne["pays_destinataire"],
                "montant": Decimal(ligne["montant"]),
                "devise": ligne["devise"]
            }

            transactions.append(transaction)

    return transactions