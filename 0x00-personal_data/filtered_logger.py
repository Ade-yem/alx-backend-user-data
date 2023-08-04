#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List
import logging
import mysql.connector
import os
import bcrypt


def filter_datum(fields: list, redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=.+?" + separator,
                         field + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor method"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database"""
    PERSONAL_DATA_DB_USERNAME = os.getenv('PERSONAL_DATA_DB_USERNAME')
    PERSONAL_DATA_DB_PASSWORD = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    PERSONAL_DATA_DB_HOST = os.getenv('PERSONAL_DATA_DB_HOST')
    PERSONAL_DATA_DB_NAME = os.getenv('PERSONAL_DATA_DB_NAME')
    cnx = mysql.connector.connection.MySQLConnection(
        user=PERSONAL_DATA_DB_USERNAME,
        password=PERSONAL_DATA_DB_PASSWORD,
        host=PERSONAL_DATA_DB_HOST,
        database=PERSONAL_DATA_DB_NAME
    )
    return cnx


def main() -> None:
    """entry"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = "name={}; email={}; phone={}; ssn={}; password={}; ".format(
            row[0], row[1], row[2], row[3], row[4], row[5])
        message += "ip={}; last_login={}; user_agent={};".format(
            row[5], row[6], row[7])
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
