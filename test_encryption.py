import sqlite3
from setup import encrypt_data, decrypt_data

DB_PATH = "data/dust5d.sqlite"

def test_encryption(wallet_address):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert encrypted test data
    test_value = "Hello, Dust5D!"
    encrypted_value = encrypt_data(test_value, wallet_address)
    cursor.execute("INSERT INTO datasets (name, encrypted_data, data_hash) VALUES (?, ?, ?)", 
                   ("test_dataset", encrypted_value, "dummy_hash"))
    conn.commit()
    print("✅ Encrypted test data inserted.")
    
    # Retrieve and decrypt test data
    cursor.execute("SELECT encrypted_data FROM datasets WHERE name = ?", ("test_dataset",))
    row = cursor.fetchone()
    if row:
        decrypted_value = decrypt_data(row[0], wallet_address)
        print(f"✅ Decryption successful: {decrypted_value}")
    else:
        print("❌ Failed to retrieve test data.")
    
    conn.close()

if __name__ == "__main__":
    test_wallet = "ban_1yog3tpzw3668xtj8jaxmk3k71ug7cf5c795sg5ximwnunppzpfq51ic9hx7"  # Replace with real wallet address
    test_encryption(test_wallet)