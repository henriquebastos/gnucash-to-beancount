from beancount.core import data
from beancount.core.account_types import DEFAULT_ACCOUNT_TYPES as ACCOUNT_TYPES


def meta_from(obj, attributes):
    d = {}
    for k in attributes.split(' '):
        v = getattr(obj, k, None)
        if not v:
            continue

        d[k] = v

    return data.new_metadata('', '', d)


def _get_account_types_map(acc_types):
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

SEP = ':'


def account_name(account):
    name = account.fullname
    name = name.replace(' ', '-')  # Beancount does not allow whitespace.

    acc_type = ACCOUNT_TYPES_MAP[account.type]
    head, _, tail = name.partition(SEP)

    if head != acc_type:
        # Filter empty parts
        parts = (part for part in (acc_type, head, tail) if part)
        name = SEP.join(parts)

    return name


def units_for(split):
    # I was having balance precision problems due to how beancount deal
    # with integer precision. So multiply quantity by 1.0 to force at
    # least 1 decimal place.

    number = split.quantity * data.Decimal('1.0')
    currency = split.account.commodity.mnemonic

    return data.Amount(number, currency)


def price_for(split):
    acc_comm = split.account.commodity
    txn_comm = split.transaction.currency

    if acc_comm == txn_comm:
        return None

    number = abs(split.value / split.quantity)
    currency = txn_comm.mnemonic

    return data.Amount(number, currency)


def Open(account, date):
    meta = meta_from(account, 'code description')
    name = account_name(account)
    commodity = [account.commodity.mnemonic] if account.commodity else None

    return data.Open(meta, date, name, commodity, None)


def Commodity(commodity, date):
    meta = meta_from(commodity, 'fullname')

    return data.Commodity(meta, date, commodity.mnemonic)


def Price(price):
    meta = {}
    date = price.date.date()
    currency = price.commodity.mnemonic
    amount = data.Amount(price.value, price.currency.mnemonic)

    return data.Price(meta, date, currency, amount)


def Transaction(txn, postings=None):
    meta = meta_from(txn, 'num notes')
    date = txn.post_date.date()
    flag = '*'
    payee = ''
    narration = txn.description

    postings = postings or []

    return data.Transaction(meta, date, flag, payee, narration, None, None, postings)


def Posting(split):
    meta = meta_from(split, 'memo')
    account = account_name(split.account)
    cost = None
    flag = None
    units = units_for(split)
    price = price_for(split)

    return data.Posting(account, units, cost, price, flag, meta)


def TransactionWithPostings(txn):
    return Transaction(txn, [Posting(split) for split in txn.splits])
