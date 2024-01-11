#!/usr/bin/env python3
"""
filterd logger solutions
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: List[str], separator: str) -> List:
    """obfuscates a message and returns it"""
    for field in fields:
        pattern = re.escape(field) + r'=[^' + re.escape(separator) + r']+'
        message = re.sub(pattern, field + '=' + redaction, message)
    return message
