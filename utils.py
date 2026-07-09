import os
from cryptography.fernet import Fernet

UPLOAD_FOLDER = "uploads"
KEY_FILE = "secret.key"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

key = load_key()
cipher = Fernet(key)

def encrypt_file(data):
    return cipher.encrypt(data)

def decrypt_file(data):
    return cipher.decrypt(data)

def save_file(data, filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, "wb") as f:
        f.write(data)

def read_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, "rb") as f:
        return f.read()