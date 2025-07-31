from Crypto.Cipher import AES
from configuration.config import SECRET_KEY
import base64
import json

def pad(data):
    block_size = AES.block_size
    padding = block_size - len(data) % block_size
    return data + (chr(padding) * padding)

def unpad(data):
    return data[:-ord(data[-1])]

def encrypt_data(data: dict):
    raw = pad(json.dumps(data)).encode()
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(raw)
    return base64.b64encode(encrypted).decode()
