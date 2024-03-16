#!/usr/bin/env python3
"""Regex-ing
"""
import re
import logging
import mysql.connector
from os import getenv
from typing import List, Optional
from mysql.connector.connection import MySQLConnection


# Personally Identifiable Fields
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """Return a logger object
    Logger name is : user_data
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    # Formatter
    formatter = RedactomgFormatter(fields=PII_FIELDS)

    # Stream Handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # use the handler
    logger.addHandler(stream_handler)

    # Should logger propagate messages to other loggers?
    logger.propagate = False

    return logger


def get_db() -> MySQLConnection:
    """Return a connection to database
    """
    database = 'holberton'
    if not getenv('PERSONAL_DATA_DB_HOST'):
        host = 'localhost'
    else:
        host = getenv('PERSONAL_DATA_DB_HOST')

    if not getenv('PERSONAL_DATA_DB_USERNAME'):
        user = 'root'
    else:
        user = getenv('PERSONAL_DATA_DB_USERNAME')

    if not getenv('PERSONAL_DATA_DB_PASSWORD'):
        password = ''
    else:
        password = getenv('PERSONAL_DATA_DB_PASSWORD')

    config = {
            'host': host, 'user': user, 'password': password,
            'database': database
            }

    # Attempt connecting to database using the above credentials
    try:
        conn = MySQLConnection(**config)
        return conn
    except mysql.connector.Error as err:
        return None
