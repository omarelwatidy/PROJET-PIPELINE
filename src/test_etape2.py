from datetime import datetime
from decimal import Decimal
from typess import Transaction
from traitement import (
    somme_par_iban_origine,
    somme_par_banque,
    somme_par_iban_destinataire,
    depasse_5000
)


transactions: list[Transaction] = [
    {"datetime_transaction": datetime(2026, 9, 1, 10, 0),"iban_origine": "FR7630006000011234567890189","pays_source": "FRANCE","banque_source": "CCF","iban_destinataire": "FR7630006345611234567890189","pays_destinataire": "FR","montant": Decimal("2000"),"devise": "EUR"},
    {
        "datetime_transaction": datetime(2026, 9, 1, 11, 0),
        "iban_origine": "FR8330006000011234567890189",
        "pays_source": "FRANCE",
        "banque_source": "CCF",
        "iban_destinataire": "FR7630006037611234567890189",
        "pays_destinataire": "FR",
        "montant": Decimal("4000"),
        "devise": "EUR"
    },
    {
        "datetime_transaction": datetime(2026, 9, 1, 12, 0),
        "iban_origine": "FR7630006037611234567890189",
        "pays_source": "FRANCE",
        "banque_source": "CCF",
        "iban_destinataire": "FR7630396037611234567890189",
        "pays_destinataire": "DE",
        "montant": Decimal("6000"),
        "devise": "EUR"
    }
]


def test_somme_par_iban_origine():
    resultat = somme_par_iban_origine(transactions)

    assert resultat == {"FR7630006000011234567890189": Decimal("2000"),"FR8330006000011234567890189": Decimal("4000"), "FR7630006037611234567890189": Decimal("6000")}


def test_somme_par_banque():
    resultat = somme_par_banque(transactions)

    assert resultat == { "CCF": Decimal("12000") }


def test_somme_par_iban_destinataire():
    resultat = somme_par_iban_destinataire(transactions)
    assert resultat == {"FR7630006345611234567890189": Decimal("2000"), "FR7630006037611234567890189": Decimal("4000"), "FR7630396037611234567890189": Decimal("6000")}

def test_depasse_5000():
    assert depasse_5000(transactions[0]) is False
    assert depasse_5000(transactions[1]) is False
    assert depasse_5000(transactions[2]) is True


if __name__ == "__main__":
    test_somme_par_iban_origine()
    test_somme_par_banque()
    test_somme_par_iban_destinataire()
    test_depasse_5000()

    print("tous les tests ont réussis")