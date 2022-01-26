import pathlib
import os
from cryptography.fernet import Fernet


def encrypt(plain_text):
    root_path = pathlib.Path().resolve()
    key_path = os.path.join(root_path, '../encryptKey.txt')

    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        txt_file = open(key_path, 'w+')
        txt_file.write(key.decode())
        txt_file.close()

    txt_file = open(key_path, 'r+')
    key = txt_file.read()
    txt_file.close()
    fernet = Fernet(str.encode(key))

    cipher_text = fernet.encrypt(str.encode(plain_text))

    return cipher_text.decode()


def decrypt(cipher_text):
    root_path = pathlib.Path().resolve()
    key_path = os.path.join(root_path, '../encryptKey.txt')

    txt_file = open(key_path, 'r+')
    key = txt_file.read()
    txt_file.close()
    fernet = Fernet(str.encode(key))

    plain_text = fernet.decrypt(cipher_text).decode()

    return plain_text
