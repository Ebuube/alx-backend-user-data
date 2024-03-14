#!/usr/bin/env python3
"""Regex-ing
"""
import re
import logging
from typing import List


def sub(m, redaction, separator):
    """Substitute a group of regex matches with redaction
    """
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


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """
    REDACTION = "***"
    # FORMAT = "[HOLBERTON] %(name) %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = []):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Return the customized format result
        """
        msg = record.msg
        record.msg = filter_datum(fields=self.fields, redaction=self.REDACTION,
                                  message=msg, separator=self.SEPARATOR)
        return super().format(record)
