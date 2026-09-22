import csv
import random
import os
from datetime import datetime, timedelta


class Compte:
    def __init__(self,iban,pays,bank,balance):
        self.iban = iban
        self.pays = pays
        self.bank = bank
        self.balance = balance

       





Lorigine = [Compte("FR7630006000011234567890189", "FRANCE", "CCF",10000),Compte("FR7630006010011234567890189", "FRANCE", "CCF",10000),Compte("FR7630006002011234567890189", "FRANCE", "CCF",10000) ]
Ldest = [Compte("FR89370400440532013000", "FRANCE", "CCF",10000),
    Compte("FR7635006002314234567890189", "FRANCE", "CCF",10000),
    Compte("FR9121000418450100051332", "FRANCE", "CCF",10000)]
def generer_csv(dossier: str) -> None:
    random.seed(42)
    devise = "EURO"

    lines = []
    date_now = datetime(2026, 9, 1, 5, 2)
    for i in range(6):
        date_now = date_now + timedelta(minutes=random.randint(10, 120))
        origine = random.choice(Lorigine)
        dest = random.choice(Ldest)

        if i == 0:
            montant = round(random.uniform(5000, 10000), 2)
        else:
            montant = round(random.uniform(100, 3000), 2)

        lines.append([
            date_now.strftime("%Y-%m-%dT%H:%M:%S"),
            origine.iban,
            origine.pays,
            origine.bank,
            dest.iban,
            dest.pays,
            f"{montant:.2f}",
            devise,
        ])

    with open(os.path.join(dossier, "transactions_2026-09-01.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "datetime_transaction",
            "iban_origine",
            "pays_source",
            "banque_source",
            "iban_destinataire",
            "pays_destinataire",
            "montant",
            "devise",
        ])
        writer.writerows(lines)

    lines2 = []
    date_actuelle = datetime(2026, 9, 9, 8, 30)

    for i in range(8):
        date_actuelle = date_actuelle + timedelta(minutes=random.randint(10, 120))
        origine = random.choice(Lorigine)
        dest = random.choice(Ldest)

        if i == 0:
            montant = round(random.uniform(5000, 12000), 2)
        else:
            montant = round(random.uniform(10, 3000), 2)

        lines2.append([
            date_actuelle.strftime("%Y-%m-%dT%H:%M:%S"),
            origine.iban,
            origine.pays,
            origine.bank,
            dest.iban,
            dest.pays,
            f"{montant:.2f}",
            devise,
        ])

    with open(os.path.join(dossier, "transactions_2026-09-09.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "datetime_transaction",
            "iban_origine",
            "pays_source",
            "banque_source",
            "iban_destinataire",
            "pays_destinataire",
            "montant",
            "devise",          
        ])
        writer.writerows(lines2)

    lines3 = []
    date_actuelle = datetime(2026, 9, 10, 14, 0)

    for i in range(5):
        date_actuelle = date_actuelle + timedelta(minutes=random.randint(10, 120))
        origine = random.choice(Lorigine)
        dest = random.choice(Ldest)
        montant = round(random.uniform(10, 3000), 2)

        lines3.append([
            date_actuelle.strftime("%Y-%m-%dT%H:%M:%S"),
            origine.iban,
            origine.pays,
            origine.bank,
            dest.iban,
            dest.pays,
            f"{montant:.2f}",
            "devise",
        ])

    with open(os.path.join(dossier, "transactions_2026-09-10.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "datetime_transaction",
            "iban_origine",
            "pays_source",
            "banque_source",
            "iban_destinataire",
            "pays_destinataire",
            "montant",
            "devise",          
        ])
        writer.writerows(lines3)