#!/usr/bin/env python3
"""
module showing how to encrypt sensitive user information
using the bcrypt library
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """func to hash and return a salted password"""
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
