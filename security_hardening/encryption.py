from cryptography.fernet import Fernet
from django.conf import settings


def get_cipher():
    key = settings.DATA_ENCRYPTION_KEY.encode()
    return Fernet(key)


def encrypt_value(value):
    if value is None:
        return None

    if value == "":
        return ""

    return get_cipher().encrypt(
        value.encode()
    ).decode()


def decrypt_value(value):
    if value is None:
        return None

    if value == "":
        return ""

    return get_cipher().decrypt(
        value.encode()
    ).decode()