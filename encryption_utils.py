
from banano_mfa import check_banano_transaction
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
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

def generate_key(wallet_address, mfa_tx_hash):
    """
    Generate and encrypt the encryption key using the wallet hash + MFA transaction hash.
    """
    if not os.path.exists(KEY_PATH):
        raw_key = Fernet.generate_key()
        secure_key = derive_secure_key(wallet_address, mfa_tx_hash)
        encrypted_key = Fernet(secure_key).encrypt(raw_key)
        
        with open(KEY_PATH, "wb") as key_file:
            key_file.write(encrypted_key)
        print("✅ Encryption key generated and locked to MFA transaction.")
    else:
        print("🔹 Encryption key already exists.")

def derive_secure_key(wallet_address, mfa_tx_hash):
    """
    Derive a cryptographically secure key using MFA transaction data.
    """
    salt = hashlib.sha256(wallet_address.encode()).digest()
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=mfa_tx_hash.encode(),
    )
    return base64.urlsafe_b64encode(hkdf.derive(wallet_address.encode()))

def load_key(wallet_address):
    """
    Validate MFA and retrieve the decrypted encryption key.
    """
    success, mfa_tx_hash = check_banano_transaction(wallet_address)
    if not success:
        raise PermissionError("❌ Access Denied: MFA verification failed.")
    
    with open(KEY_PATH, "rb") as key_file:
        encrypted_key = key_file.read()
    secure_key = derive_secure_key(wallet_address, mfa_tx_hash)
    return Fernet(secure_key).decrypt(encrypted_key)

