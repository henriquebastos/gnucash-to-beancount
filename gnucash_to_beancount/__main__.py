import argparse
from operator import attrgetter
from pathlib import Path

import piecash
from beancount.parser import printer

from gnucash_to_beancount.convert import ACCOUNT_TYPES
from gnucash_to_beancount.convert import Commodity
from gnucash_to_beancount.convert import Open
from gnucash_to_beancount.convert import Price
from gnucash_to_beancount.convert import TransactionWithPostings


def file_exists(filename):
    if not Path(filename).exists():
        raise argparse.ArgumentTypeError('File not found: ' + filename)

    return filename


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=file_exists)

    return parser.parse_args()


def main(options):
    with piecash.open_book(options.input, readonly=True) as book:
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

    printer.print_entries(entries)


main(parse_arguments())
