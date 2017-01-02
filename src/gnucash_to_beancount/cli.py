"""Gnucash to Beancount converter.
"""

import argparse
from pathlib import Path

import piecash
from beancount.parser import printer
from gnucash_to_beancount import convert

__author__ = "Henrique Bastos <henrique@bastos.net>"
__license__ = "GNU GPLv2"


def file_exists(filename):
    """Make sure input filename exists."""
    if not Path(filename).exists():
        raise argparse.ArgumentTypeError('File not found: ' + filename)

    return filename


def args():
    """Process the command line."""
    parser = argparse.ArgumentParser(
        description='Gnucash to Beancount Converter.',
        epilog='The Beancount ledger will be writen to STDOUT.'
    )
    parser.add_argument('filename', type=file_exists, help='Gnucash Sqlite3 file.')

    return parser.parse_args()


def main():
    """Generate beancount output from gnucash file."""
    options = args()

    with piecash.open_book(options.filename, open_if_lock=True) as book:
        entries = convert.load_entries(book)
        printer.print_entries(entries)
