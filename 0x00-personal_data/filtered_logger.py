#!/usr/bin/env python3
"""
filterd logger solutions
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: List[str], separator: str) -> List:
    """function that obfuscates a message and returns it"""
    for field in fields:
        pattern = re.escape(field) + r'=[^' + re.escape(separator) + r']+'
        message = re.sub(pattern, field + '=' + redaction, message)
    return message
