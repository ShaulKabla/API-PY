import os
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_key_to_file(key, filename):
    filepath = os.path.abspath(filename)
    with open(filepath, "wb") as key_file:
        key_file.write(key)

def load_key_from_file(filename):
    with open(filename, "rb") as key_file:
        return key_file.read()

def encrypt_api(key, data):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def decrypt_api(key, encrypted_data):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

key = generate_key()

save_key_to_file(key, "keys.txt")

loaded_key = load_key_from_file("keys.txt")


clientid = ""
secretkey = ""

encrypted_client = encrypt_api(key, clientid)
encrypted_secret = encrypt_api(key, secretkey)

decrypted_client = decrypt_api(key, encrypted_client)
decrypted_secret = decrypt_api(key, encrypted_secret)
