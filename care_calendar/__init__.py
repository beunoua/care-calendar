"""Top-level package for Care Calendar."""

__author__ = """beunoua"""
__email__ = 'beunoua'
__version__ = '0.1.0'

import datetime

def current_year() -> int:
    return datetime.datetime.now().year
