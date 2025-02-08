
from banano_mfa import check_banano_transaction
from cryptography.fernet import Fernet
import hashlib
import base64
import os

KEY_PATH = "keys/encryption.key.enc"

def encrypt_data(data, wallet_address):
    """Encrypts data using the MFA-protected encryption key."""
    key = load_key(wallet_address)
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data, wallet_address):
    """Decrypts data using the MFA-protected encryption key."""
    key = load_key(wallet_address)
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

def load_key(wallet_address):
    """
    Validate MFA and retrieve the decrypted encryption key.
    """
    success, message = check_banano_transaction(wallet_address)
    if not success:
        raise PermissionError("❌ Access Denied: MFA verification failed.")
    
    with open(KEY_PATH, "rb") as key_file:
        encrypted_key = key_file.read()
    wallet_hash = generate_wallet_hash(wallet_address)
    return Fernet(wallet_hash).decrypt(encrypted_key)

def generate_wallet_hash(wallet_address):
    """
    Generate a Base64-encoded SHA-256 hash based on the wallet address.
    This will be used as part of the encryption key reconstruction.
    """
    hash_bytes = hashlib.sha256(wallet_address.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes[:32])  # Ensure proper length

def generate_key(wallet_address):
    """
    Generate and encrypt the encryption key using the wallet hash.
    """
    if not os.path.exists(KEY_PATH):
        raw_key = Fernet.generate_key()
        wallet_hash = generate_wallet_hash(wallet_address)
        encrypted_key = Fernet(wallet_hash).encrypt(raw_key)
        
        with open(KEY_PATH, "wb") as key_file:
            key_file.write(encrypted_key)
        print("✅ Encryption key generated and locked to wallet.")
    else:
        print("🔹 Encryption key already exists.")

def load_key(wallet_address):
    """
    Validate MFA and retrieve the decrypted encryption key.
    """
    success, message = check_banano_transaction(wallet_address)
    if not success:
        raise PermissionError("❌ Access Denied: MFA verification failed.")
    
    with open(KEY_PATH, "rb") as key_file:
        encrypted_key = key_file.read()
    wallet_hash = generate_wallet_hash(wallet_address)
    return Fernet(wallet_hash).decrypt(encrypted_key)
