import hashlib
import os
import bcrypt


def password_hash(password):
    p_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(p_bytes, salt)
    return hashed


def password_validation(password, phashed):
    password_encode = password.encode('utf-8')

    check = bcrypt.checkpw(password_encode, phashed)
    return check
