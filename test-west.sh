#!/usr/bin/env bash

# A first primitive golden file test.

diff data/sample-west.beancount <(gnucash-to-beancount data/sample.gnucash) &&
diff data/sample-west-bean-report-accounts.txt <(bean-report data/sample-west.beancount accounts) &&
diff data/sample-west-bean-report-balances.txt <(bean-report data/sample-west.beancount balances) &&
diff data/sample-west-bean-report-stats-postings.txt <(bean-report data/sample-west.beancount stats-postings) &&
diff data/sample-west-bean-report-stats-types.txt <(bean-report data/sample-west.beancount stats-types)
