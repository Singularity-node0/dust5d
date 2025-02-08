import sqlite3
import os
import hashlib
import base64
from cryptography.fernet import Fernet
from banano_mfa import check_banano_transaction

# Define paths
DB_PATH = "data/dust5d.sqlite"
KEY_PATH = "keys/encryption.key.enc"
SCHEMA_PATHS = [
    "schema/dataset_schema.sql",
    "schema/access_control_schema.sql"
]

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

def initialize_database(wallet_address):
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Load schema files
        for schema in SCHEMA_PATHS:
            with open(schema, "r") as f:
                cursor.executescript(f.read())
                print(f"✅ Schema {schema} applied.")

        conn.commit()
        conn.close()
        print("✅ Database initialized.")
    else:
        print("🔹 Database already exists.")

if __name__ == "__main__":
    test_wallet = "ban_1xyz..."  # Replace with real wallet address
    print("🚀 Initializing Dust5D Node with MFA-Locked Encryption...")
    generate_key(test_wallet)
    initialize_database(test_wallet)
    print("✅ Dust5D Node setup complete with MFA-protected encryption key.")