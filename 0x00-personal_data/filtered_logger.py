#!/usr/bin/env python3
"""Regex-ing
"""
import re
from typing import List

def filter_datum(fields: List[str] = [], rep: str = 'xxx', msg: str ='',
        sep: str =';') -> str:
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
