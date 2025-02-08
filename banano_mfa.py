import requests
import time
import json

BANANO_RPC_URL = "https://kaliumapi.appditto.com/api"
MFA_VALIDITY_PERIOD = 600  # 10 minutes

def check_banano_transaction(wallet_address, dataset_id):
    """
    Check if a valid MFA transaction exists for the given wallet address.
    """
    payload = {
        "action": "account_history",
        "account": wallet_address,
        "count": 10
    }
    
    response = requests.post(BANANO_RPC_URL, json=payload)
    data = response.json()
    
    if "history" not in data:
        return False, "No transaction history found."
    
    for tx in data["history"]:
        # Extract transaction details
        tx_time = int(tx["local_timestamp"])
        tx_amount = int(tx["amount"])
        tx_hash = tx["hash"]
        
        # Validate transaction timing
        if time.time() - tx_time > MFA_VALIDITY_PERIOD:
            continue  # Ignore old transactions
        
        # Verify dataset ID in transaction metadata (if applicable)
        # Assume metadata is encoded in the transaction note/comment
        if dataset_id not in tx.get("block_account", ""):
            continue
        
        return True, f"Valid MFA transaction found: {tx_hash}"
    
    return False, "No valid MFA transaction found."

if __name__ == "__main__":
    test_wallet = "ban_19rzir87uw13tc6pt7kc97pipr8jtxopbiwtgzmoycm1kope66aar59h95sc"  # Replace with a real wallet address
    test_dataset_id = "123"
    success, message = check_banano_transaction(test_wallet, test_dataset_id)
    print(f"MFA Verification Result: {message}")
