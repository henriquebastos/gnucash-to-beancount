"""Factories to transform Gnucash entities into Beancount directives.
"""
from beancount.core import data
from beancount.core.account_types import DEFAULT_ACCOUNT_TYPES as ACCOUNT_TYPES

__author__ = "Henrique Bastos <henrique@bastos.net>"
__license__ = "GNU GPLv2"


def meta_from(obj, fields):
    """Build a meta dict from fields that have values."""
    return {k: v
            for k in fields.split(' ')
            for v in (getattr(obj, k),)
            if v}


# Accounts & Open


def _get_account_types_map(acc_types):
    """Helper that maps account types from Gnucash to Beancount.

    Gnucash have 1 root account and 13 account types allowing very
    permissive account trees.

    However, Beancount restrict us to 5 root account types.

    So we need to build a map that will help us fix the account tree.
    """
    pairs = (
        ('ROOT', None),
        ('ASSET BANK CASH MUTUAL RECEIVABLE STOCK TRADING', acc_types.assets),
        ('EQUITY', acc_types.equity),
        ('EXPENSE', acc_types.expenses),
        ('INCOME', acc_types.income),
        ('LIABILITY CREDIT PAYABLE', acc_types.liabilities),
    )

    return {gnc: bc for seq, bc in pairs for gnc in seq.split(' ')}


ACCOUNT_TYPES_MAP = _get_account_types_map(ACCOUNT_TYPES)
ACCOUNT_SEP = ':'

def fix_account_name_part(part):
    # Beancount account name parts cannot start with a digit
    if part[0].isdigit(): return 'X-' + part
    # Nor can they start with a '-'
    if part[0] == '-': return 'X' + part
    # Nor can they start with lower case
    return part[0].upper() + part[1:]

def account_name(account):
    """Returns a valid Beancount account name for a Gnucash account."""

    name = account.fullname
    name = sanitize_name(name)

    # Beancount account names cannot start with lower case
    name = ACCOUNT_SEP.join(list(map(lambda part: fix_account_name_part(part), name.split(ACCOUNT_SEP))))

    # If the Gnucash account is not under a valid Beancount account root
    # we must append it to the proper branch using the built account map.
    acc_type = ACCOUNT_TYPES_MAP[account.type]
    head, _, tail = name.partition(ACCOUNT_SEP)

    if head != acc_type:
        # Filter empty parts
        parts = (p for p in (acc_type, head, tail) if p)
        name = ACCOUNT_SEP.join(parts)

    return name

def sanitize_name(name):

    name = name.replace(' ', '-')  # Beancount does not allow whitespace.

    name = name.replace('@', 'at')
    name = name.replace('%', 'pct')
    name = name.replace('.', 'dot')
    name = name.replace('&', 'and')
    name = name.replace('+', 'plus')
    name = name.replace('?', 'q')
    name = name.replace('¢', 'cent')

    name = name.replace("'", '')  # Joe's -> Joes
    name = name.replace('(', '')
    name = name.replace(')', '')  # 401(k) -> 401k
    name = name.replace(',', '')  # A, B & C -> A-B-and-C
    name = name.replace('*', '')  # Macy*s -> Macys

    name = name.replace('/', '-')
    name = name.replace('_', '-')

    return name



def Open(account, date):
    meta = meta_from(account, 'code description')
    name = account_name(account)
    commodity = [commodity_name(account.commodity)] if account.commodity else None

    return data.Open(meta, date, name, commodity, None)

def commodity_name(commodity):
    """Returns a valid Beancount commodity name for a Gnucash commodity"""

    name = sanitize_name(commodity.mnemonic)

    # According to the documentation
    # name can be up to 24 characters long, beginning with a capital letter and ending with a capital letter or a number.
    # Leading initially to
    #    name = name[0].upper() + name[1:24]
    # But it seems that it must be all upper case
    name = name.upper()[:24]
    # TODO: "and ending with a capital letter or a number." we may have a - at the end

    return name


def Commodity(commodity, date):
    meta = meta_from(commodity, 'fullname')
    name = commodity_name(commodity)

    return data.Commodity(meta, date, name)


def Price(price):
    meta = {}
    date = price.date.date()
    currency = commodity_name(price.commodity)
    amount = data.Amount(price.value, currency)

    return data.Price(meta, date, currency, amount)


# Postings


def units_for(split):
    # I was having balance precision problems due to how beancount deal
    # with integer precision. So multiply quantity by 1.0 to force at
    # least 1 decimal place.

    number = split.quantity * data.Decimal('1.0')
    currency = commodity_name(split.account.commodity)

    return data.Amount(number, currency)


def price_for(split):
    acc_comm = split.account.commodity
    txn_comm = split.transaction.currency

    if acc_comm == txn_comm:
        return None

    number = abs(split.value / split.quantity)
    currency = commodity_name(txn_comm)

    return data.Amount(number, currency)


def Posting(split):
    meta = meta_from(split, 'memo')
    account = account_name(split.account)
    cost = None
    flag = None
    units = units_for(split)
    price = price_for(split)

    return data.Posting(account, units, cost, price, flag, meta)


def Transaction(txn, postings=None):
    meta = meta_from(txn, 'num notes')
    date = txn.post_date.date()
    flag = '*'
    payee = ''
    narration = txn.description

    postings = postings or []

    return data.Transaction(meta, date, flag, payee, narration, None, None, postings)


def TransactionWithPostings(txn):
    return Transaction(txn, [Posting(split) for split in txn.splits])
