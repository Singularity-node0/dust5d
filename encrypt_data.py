import sqlite3
from encryption_utils import encrypt_data

DB_PATH = "data/dust5d.sqlite"

def insert_encrypted_data(wallet_address, dataset_name, raw_data):
    """
    Encrypts and inserts data into the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    encrypted_value = encrypt_data(raw_data, wallet_address)
    cursor.execute("INSERT INTO datasets (name, encrypted_data, data_hash) VALUES (?, ?, ?)", 
                   (dataset_name, encrypted_value, "dummy_hash"))
    conn.commit()
    conn.close()
    print(f"✅ Data inserted successfully for dataset: {dataset_name}")

if __name__ == "__main__":
    test_wallet = "ban_1yog3tpzw3668xtj8jaxmk3k71ug7cf5c795sg5ximwnunppzpfq51ic9hx7"  # Replace with real wallet address
    dataset_name = "test_dataset"
    raw_data = "This is some secret data."
    insert_encrypted_data(test_wallet, dataset_name, raw_data)