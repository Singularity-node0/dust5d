import sqlite3
from setup import encrypt_data, decrypt_data

DB_PATH = "data/dust5d.sqlite"

def test_encryption():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert encrypted test data
    test_value = "Hello, Dust5D!"
    encrypted_value = encrypt_data(test_value)
    cursor.execute("INSERT INTO datasets (name, encrypted_data, data_hash) VALUES (?, ?, ?)", 
                   ("test_dataset", encrypted_value, "dummy_hash"))
    conn.commit()
    print("✅ Encrypted test data inserted.")
    
    # Retrieve and decrypt test data
    cursor.execute("SELECT encrypted_data FROM datasets WHERE name = ?", ("test_dataset",))
    row = cursor.fetchone()
    if row:
        decrypted_value = decrypt_data(row[0])
        print(f"✅ Decryption successful: {decrypted_value}")
    else:
        print("❌ Failed to retrieve test data.")
    
    conn.close()

if __name__ == "__main__":
    test_encryption()
