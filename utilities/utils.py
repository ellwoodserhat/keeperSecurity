from Crypto.Cipher import AES
from configuration.config import SECRET_KEY
import base64
import json
import logging

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

def decrypt_data(enc_data: str):
    try:
        encrypted = base64.b64decode(enc_data)
        cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted)
        unpadded = unpad(decrypted.decode())
        return json.loads(unpadded)
    except Exception as e:
        get_logger().error(f"Decryption failed: {e}")
        return {}

def get_logger(name="api_logger"):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
