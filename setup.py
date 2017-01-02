# coding: utf-8
from setuptools import setup, find_packages
import os


README = os.path.join(os.path.dirname(__file__), 'README.rst')


if __name__ == "__main__":
    setup(name='gnucash-to-beancount',
          description='Gnucash to Beancount Converter.',
          version='1.0b0',
          long_description=open(README).read(),
          author="Henrique Bastos", author_email="henrique@bastos.net",
          license="GNU GPLv2 only",
          url='http://github.com/henriquebastos/gnucash-to-beancount/',
          keywords=['beancount', 'gnucash', 'convert', 'converter', 'ledger', 'accounting'],
          install_requires=[
              'beancount',
              'piecash',
          ],
          packages=find_packages(where='src'),
          package_dir={"": "src"},
          entry_points={
              'console_scripts': [
                  'gnucash-to-beancount = gnucash_to_beancount.cli:main',
              ]
          },
          zip_safe=False,
          platforms='any',
          include_package_data=True,
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: Financial and Insurance Industry',
              'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
              'Natural Language :: English',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3 :: Only',
              'Topic :: Office/Business :: Financial :: Accounting',
              'Topic :: Utilities',
          ])
