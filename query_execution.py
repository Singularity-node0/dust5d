import sqlite3
from banano_mfa import check_banano_transaction

DB_PATH = "data/dust5d.sqlite"

def execute_query(wallet_address, query):
    """
    Executes a database query only if the wallet address has a valid MFA transaction.
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
        return f"✅ Query Successful: {result}"
    except Exception as e:
        return f"❌ Query Error: {str(e)}"

if __name__ == "__main__":
    test_wallet = "ban_1yog3tpzw3668xtj8jaxmk3k71ug7cf5c795sg5ximwnunppzpfq51ic9hx7"  # Replace with real wallet address
    test_query = "SELECT * FROM datasets;"
    result = execute_query(test_wallet, test_query)
    print(result)
