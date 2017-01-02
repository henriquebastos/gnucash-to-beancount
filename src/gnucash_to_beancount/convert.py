"""The logic that builds a Beancount entry list from Gnucash entities.
"""
from operator import attrgetter

from gnucash_to_beancount.directives import ACCOUNT_TYPES
from gnucash_to_beancount.directives import Commodity
from gnucash_to_beancount.directives import Open
from gnucash_to_beancount.directives import Price
from gnucash_to_beancount.directives import TransactionWithPostings

__author__ = "Henrique Bastos <henrique@bastos.net>"
__license__ = "GNU GPLv2"


def load_entries(book):
    first_date = book.transactions[0].post_date.date()

    entries = []

    for account in book.accounts:
        if account.fullname in ACCOUNT_TYPES:
            continue

        entries.append(Open(account, first_date))

    entries.sort(key=attrgetter('account'))

    for commodity in book.commodities:
        entries.append(Commodity(commodity, first_date))

    for price in book.prices:
        entries.append(Price(price))

    for txn in book.transactions:
        entries.append(TransactionWithPostings(txn))

    return entries
