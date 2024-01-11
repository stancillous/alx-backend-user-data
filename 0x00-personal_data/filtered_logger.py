#!/usr/bin/env python3
"""
filterd logger solutions
"""
from typing import List
from os import environ
import re
from mysql.connector import connection


def filter_datum(fields: List[str], redaction: str,
                 message: List[str], separator: str) -> List:
    """function that obfuscates a message and returns it"""
    for field in fields:
        pattern = re.escape(field) + r'=[^' + re.escape(separator) + r']+'
        message = re.sub(pattern, field + '=' + redaction, message)
    return message


def get_db():
    """func that returns a connector to a database"""
    # config = {
    #     "user": os.getenv("PERSONAL_DATA_DB_USERNAME"),
    #     "host": os.getenv("PERSONAL_DATA_DB_HOST"),
    #     "password": os.getenv("PERSONAL_DATA_DB_PASSWORD"),
    #     "database": os.getenv("PERSONAL_DATA_DB_NAME")
    # }
    # connection_obj = connection.MySQLConnection(**config)
    # return connection_obj
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    cnx = connection.MySQLConnection(user=username,
                                     password=password,
                                     host=host,
                                     database=db_name)
    return cnx
