import sqlite3
from encryption_utils import encrypt_data
from db_utils import insert_encrypted_data

if __name__ == "__main__":
    test_wallet = "ban_1yog3tpzw3668xtj8jaxmk3k71ug7cf5c795sg5ximwnunppzpfq51ic9hx7"  # Replace with real wallet address
    dataset_name = "test_dataset"
    raw_data = "1ban = 1ban"
    insert_encrypted_data(test_wallet, dataset_name, raw_data)