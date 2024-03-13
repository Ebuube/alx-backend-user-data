#!/usr/bin/env python3
"""Regex-ing
"""
import re
from typing import List


def sub(m, redaction, separator):
    return f"{m.group('field')}={redaction}{separator}"


def filter_datum(fields: List[str] = [], redaction: str = 'xxx',
                 message: str = '', separator: str = ';') -> str:
    """Obfuscate sensitive fields in a log line
    redaction: redactionlacment string
    message: message to obfuscate
    separator: separators to use
    Pattern -> '{field}={val}(optional semicolon)'
    """
    for field in fields:
        pattern = '(?P<field>{})=(?P<val>.*?)(?:{}|$)'.format(field, separator)
        message = re.sub(pattern,
                         lambda m: sub(m, redaction, separator), message)
    return message
