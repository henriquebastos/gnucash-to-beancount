"""Gnucash to Beancount converter.
"""
import sys

__author__ = "Henrique Bastos <henrique@bastos.net>"
__license__ = "GNU GPLv2"


if sys.version_info < (3, 3):
    raise ImportError("Python 3.3 or above is required.")
