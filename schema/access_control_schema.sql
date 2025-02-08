-- Access Control Table Schema
    CREATE TABLE access_control (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id INTEGER NOT NULL,
        wallet_address TEXT NOT NULL,
        permission_type TEXT CHECK(permission_type IN ('read', 'write')) NOT NULL,
        transaction_hash TEXT NOT NULL,
        granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(dataset_id) REFERENCES datasets(id)
    );