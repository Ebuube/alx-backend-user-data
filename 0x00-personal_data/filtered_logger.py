#!/usr/bin/env python3
"""Regex-ing
"""
import re


def filter_datum(fields=[], replacement='xxx', message='', separator=';'):
    """Obfuscate sensitive fields in a log line
    """
    if not message or len(message) < 1:
        return ''
    for field in fields:
        pattern = '(?P<fieldname>{})=(?P<value>.*?)(?:;|$)'.format(field) # '{fieldname}={value}[;]'
        message = re.sub(pattern, lambda m: f"{m.group('fieldname')}={replacement};", message)
    return message
