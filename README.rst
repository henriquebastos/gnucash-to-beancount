Gnucash to Beancount Converter
==============================

Convert your Gnucash Sqlite3 file to a Beancount text ledger.

*Requires Python 3.3+*

Install
-------

.. code-block:: console

    pip install gnucash-to-beancount

Usage
-----

.. code-block:: console

 gnucash-to-beancount my-ledger.gnucash > my-ledger.beancount

Development
-----------

.. code-block:: console

 git clone https://github.com/henriquebastos/gnucash-to-beancount.git
 cd gnucash-to-beancount
 python -m venv -p python3.6 .venv
 source .venv/bin/activate
 python setup.py develop
 ./test.sh

The tests are still primitives using `diff` with *golden files*. If
`test.sh` shows nothing, all is good. :)

If `test.sh` shows errors where dates are off by one, try using `test-west.sh` instead.

Known Limitations
=================

This version supports:

- Accounts
- Transactions and it's Splits
- Commodities
- Prices

Unsupported features:

- Lots
- Budget
- Scheduled Transactions
- All Business entities
- Key Value metadata

You may help improve this project by providing a sample Gnucash Sqlite3
file that uses one or more unsupported features.

License
=======

Copyright (C) 2017 Henrique Bastos.

This code is distributed under the terms of the "GNU GPLv2 only". See LICENSE file for details.
