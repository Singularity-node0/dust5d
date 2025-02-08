import sqlite3
import os
import hashlib
import base64
from cryptography.fernet import Fernet
from banano_mfa import check_banano_transaction
from encryption_utils import encrypt_data, decrypt_data, generate_key

# Define paths
DB_PATH = "data/dust5d.sqlite"
KEY_PATH = "keys/encryption.key.enc"
SCHEMA_PATHS = [
    "schema/dataset_schema.sql",
    "schema/access_control_schema.sql"
]

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
    test_wallet = "ban_1yog3tpzw3668xtj8jaxmk3k71ug7cf5c795sg5ximwnunppzpfq51ic9hx7"  # Replace with real wallet address
    print("🚀 Initializing Dust5D Node with MFA-Locked Encryption...")
    generate_key(test_wallet)
    initialize_database(test_wallet)
    print("✅ Dust5D Node setup complete with MFA-protected encryption key.")