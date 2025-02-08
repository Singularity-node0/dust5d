import sqlite3
from banano_mfa import check_banano_transaction
from encryption_utils import encrypt_data, decrypt_data

DB_PATH = "data/dust5d.sqlite"

def execute_query(wallet_address, query, decrypt_result=True):
    """
    Executes a database query only if the wallet address has a valid MFA transaction.
    Enforces encryption/decryption of stored data.
    """
    success, message = check_banano_transaction(wallet_address)
    if not success:
        return f"❌ Access Denied: {message}"
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        
        if decrypt_result:
            decrypted_result = [(decrypt_data(row[0], wallet_address),) if isinstance(row[0], bytes) else row for row in result]
            return f"✅ Query Successful: {decrypted_result}"
        
        return f"✅ Query Successful: {result}"
    except Exception as e:
        return f"❌ Query Error: {str(e)}"

def insert_encrypted_data(wallet_address, dataset_name, raw_data):
    """
    Encrypts and inserts or updates data into the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    encrypted_value = encrypt_data(raw_data, wallet_address)
    cursor.execute("INSERT OR REPLACE INTO datasets (name, encrypted_data, data_hash) VALUES (?, ?, ?)", 
                   (dataset_name, encrypted_value, "dummy_hash"))
    conn.commit()
    conn.close()
    print(f"✅ Data inserted/updated successfully for dataset: {dataset_name}")
