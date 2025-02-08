import sqlite3
import os
from cryptography.fernet import Fernet

# Define paths
DB_PATH = "data/dust5d.sqlite"
KEY_PATH = "keys/encryption.key"
SCHEMA_PATHS = [
    "schema/dataset_schema.sql",
    "schema/access_control_schema.sql"
]

def generate_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as key_file:
            key_file.write(key)
        print("✅ Encryption key generated.")
    else:
        print("🔹 Encryption key already exists.")

def load_key():
    with open(KEY_PATH, "rb") as key_file:
        return Fernet(key_file.read())

def initialize_database():
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

def encrypt_data(data):
    """Encrypts data using the generated encryption key."""
    f = load_key()
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data):
    """Decrypts data using the generated encryption key."""
    f = load_key()
    return f.decrypt(encrypted_data).decode()

if __name__ == "__main__":
    print("🚀 Initializing Dust5D Node with Encryption...")
    generate_key()
    initialize_database()
    print("✅ Dust5D Node setup complete with encryption.")
