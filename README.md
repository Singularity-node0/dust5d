# Dust5D Node

## Overview
This is a federated knowledge node for the Dust5D network, using SQLite for encrypted data storage and Banano DAG for access verification.

## Structure
- **data/** → Stores encrypted SQLite database (`dust5d.sqlite`)
- **schema/** → SQL schema definitions
- **queries/** → Example access queries
- **keys/** → Encryption keys & authentication records
- **logs/** → Access logs

## Setup
1. Install dependencies:
   ```sh
   pip install cryptography sqlite3
   ```
2. Start using the database:
   ```sh
   python3 scripts/setup.py
   ```

## Banano MFA Authentication
To access data, a user must send a Banano transaction that gets verified on the DAG.

---

**Next Steps:** Push this repo to GitHub, integrate Banano verification, and test MFA-based data access.
