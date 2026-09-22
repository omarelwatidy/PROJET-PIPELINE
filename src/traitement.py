from decimal import Decimal
from typess import Transaction
from typing import TypedDict
def somme_par_iban_origine(transactions: list[Transaction]) -> dict[str, Decimal]:
    results = {}
    for t in transactions:
        iban = t["iban_origine"]
        montant = t["montant"]
        if iban not in results:
            results[iban] = Decimal("0")
        results[iban] += montant

    return results
def somme_par_banque(transactions: list[Transaction]) -> dict[str, Decimal]:

    results: dict[str, Decimal] = {}

    for transaction in transactions:
        banque = transaction["banque_source"]
        montant = transaction["montant"]
        if banque not in results:
            results[banque] = Decimal("0")

        results[banque] += montant

    return results

def somme_par_iban_destinataire(transactions: list[Transaction]) -> dict[str, Decimal]:
    results = {}
    for t in transactions:
        iban = t["iban_destinataire"]
        montant = t["montant"]
        if iban not in results:
            results[iban] = Decimal("0")

        results[iban] += montant

    return results


def depasse_5000(transaction: Transaction) -> bool:
    return transaction["montant"] > 5000

