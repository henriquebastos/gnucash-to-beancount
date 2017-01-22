#!/usr/bin/env bash

# A first primitive golden file test.

diff data/sample-west.beancount <(gnucash-to-beancount data/sample.gnucash) &&
diff data/sample-bean-report-accounts.txt <(bean-report data/sample.beancount accounts) &&
diff data/sample-bean-report-balances.txt <(bean-report data/sample.beancount balances) &&
diff data/sample-bean-report-stats-postings.txt <(bean-report data/sample.beancount stats-postings) &&
diff data/sample-bean-report-stats-types.txt <(bean-report data/sample.beancount stats-types)
