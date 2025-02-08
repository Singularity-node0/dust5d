import requests
import time
import json

BANANO_RPC_URL = "https://kaliumapi.appditto.com/api"
MFA_VALIDITY_PERIOD = 600  # 10 minutes
MFA_VERIFICATION_ADDRESS = "ban_19rzir87uw13tc6pt7kc97pipr8jtxopbiwtgzmoycm1kope66aar59h95sc"  # Hardcoded MFA verification wallet

def check_banano_transaction(wallet_address):
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
        tx_destination = tx["account"]
        tx_hash = tx["hash"]
        
        # Validate transaction timing
        if time.time() - tx_time > MFA_VALIDITY_PERIOD:
            continue  # Ignore old transactions
        
        # Verify if transaction was sent to the hardcoded MFA verification address
        if tx_destination == MFA_VERIFICATION_ADDRESS:
            return True, f"Valid MFA transaction found: {tx_hash}"
    
    return False, "No valid MFA transaction found."

if __name__ == "__main__":
    test_wallet = "ban_1yog3tpzw3668xtj8jaxmk3k71ug7cf5c795sg5ximwnunppzpfq51ic9hx7"  # Replace with a real wallet address
    success, message = check_banano_transaction(test_wallet)
    print(f"MFA Verification Result: {message}")
