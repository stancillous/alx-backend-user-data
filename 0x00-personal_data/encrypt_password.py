#!/usr/bin/env python3
"""
module showing how to encrypt sensitive user information
using the bcrypt library
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """func to hash and return a salted password"""
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    print("hashed => ", hashed)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """used to validate that the provided password
    matches the hashed password"""
    password = password.encode()
    return bcrypt.checkpw(password, hashed_password)
