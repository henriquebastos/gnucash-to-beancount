"""The logic that builds a Beancount entry list from Gnucash entities.
"""
from operator import attrgetter

from gnucash_to_beancount.directives import ACCOUNT_TYPES
from gnucash_to_beancount.directives import Commodity
from gnucash_to_beancount.directives import Open
from gnucash_to_beancount.directives import Close
from gnucash_to_beancount.directives import Price
from gnucash_to_beancount.directives import TransactionWithPostings

__author__ = "Henrique Bastos <henrique@bastos.net>"
__license__ = "GNU GPLv2"


def load_entries(book):
    first_date = book.transactions[0].post_date

    entries = []

    for account in book.accounts:
        if account.fullname in ACCOUNT_TYPES or account.placeholder:
            continue

        entries.append(Open(account, first_date))

    entries.sort(key=attrgetter('account'))

    close_entries = []
    for account in book.accounts:
        if account.fullname in ACCOUNT_TYPES or account.placeholder or not account.hidden:
            continue
        close_entries.append(Close(account, first_date))

    close_entries.sort(key=attrgetter('account'))
    entries.extend(close_entries)

    for commodity in book.commodities:
        entries.append(Commodity(commodity, first_date))

    for price in book.prices:
        if price.value > 0:
            entries.append(Price(price))

    for txn in book.transactions:
        entries.append(TransactionWithPostings(txn))

    return entries
