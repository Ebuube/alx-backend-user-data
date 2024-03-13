#!/usr/bin/env python3
"""Regex-ing
"""
import re


def filter_datum(fields=[], rep='xxx', msg='', sep=';'):
    """Obfuscate sensitive fields in a log line
    rep: replacment string
    msg: message to obfuscate
    sep: separators to use
    Pattern -> '{field}={val}(optional semicolon)'
    """
    for field in fields:
        pattern = '(?P<field>{})=(?P<val>.*?)(?:;|$)'.format(field)
        msg = re.sub(pattern, lambda m: f"{m.group('field')}={rep}{sep}", msg)
    return msg
