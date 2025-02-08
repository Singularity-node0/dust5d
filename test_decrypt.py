import sqlite3
from banano_mfa import check_banano_transaction
from encryption_utils import encrypt_data, decrypt_data
from db_utils import execute_query

if __name__ == "__main__":
    test_wallet = "ban_1yog3tpzw3668xtj8jaxmk3k71ug7cf5c795sg5ximwnunppzpfq51ic9hx7"  # Replace with real wallet address
    test_query = "SELECT encrypted_data FROM datasets WHERE name = 'test_dataset';"
    result = execute_query(test_wallet, test_query)
    print(result)
