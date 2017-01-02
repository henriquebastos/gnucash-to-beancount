import argparse
from pathlib import Path

import piecash
from beancount.parser import printer
from gnucash_to_beancount import convert



def file_exists(filename):
    if not Path(filename).exists():
        raise argparse.ArgumentTypeError('File not found: ' + filename)

    return filename


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=file_exists)

    return parser.parse_args()


def main(options):
    """Generate beancount output from gnucash file."""
    with piecash.open_book(options.input, open_if_lock=True) as book:
        entries = convert.load_entries(book)
        printer.print_entries(entries)


main(cli())
