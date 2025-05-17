import json
import hashlib
import os

# Implementation of consensus protocol (proof-of-authority) for the Warehouse supply-chain System 

# Load key data from list_of_keys.json and generate RSA key pairs for all inventories
def generate_all_keypairs():
    with open('list_of_keys.json', 'r') as keys_file:
        warehouse_keys = json.load(keys_file)
    
    keypairs = {}
    for name in['inventory_a_keys', 'inventory_b_keys', 'inventory_c_keys', 'inventory_d_keys']:
        values = warehouse_keys[name]
        p = values['p']
        q = values['q']
        e = values['e']
        n = p * q
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        keypairs[name] = {
            "public_key": {"e": e, "n": n},
            "private_key": {"d": d, "n": n}
        }
    return keypairs

# Hash the record using MD5 and return in decimal format
def md5_to_decimal(record_string):
    md5_hash = hashlib.md5(record_string.encode()).hexdigest()
    return int(md5_hash, 16)

# Sign the message
def sign_message(message, private_key):
    m = md5_to_decimal(message)
    return pow(m, private_key["d"], private_key["n"])

# Verify the message
def verify_signature(message, signature, public_key):
    m = md5_to_decimal(message)
    return pow(signature, public_key["e"], public_key["n"]) == m

# Voting logic for PoA
def vote_on_record(record_string, keypair):
    signature = sign_message(record_string, keypair["private_key"])
    return verify_signature(record_string, signature, keypair["public_key"])

# Store the record to inventory files
def store_record_to_inventories(record_string):
    inventories = ['a', 'b', 'c', 'd']
    for inv in inventories:
        filename = f'inventory_{inv}.json'
        key = f'inventory_{inv}'
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {key: {}}
        
        index = str(len(data.get(key, {})))
        data[key][index] = record_string
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

# Run the PoA consensus
def run_poa_consensus(record_string, chosen_inventory):
    if not record_string or record_string[-1] not in ['A', 'B', 'C', 'D']:
        return False, 0
    
    if not record_string[:-1].isdigit():
        return False, 0
    
    keypairs = generate_all_keypairs()
    approvals = 0

    for inv_key, pair in keypairs.items():
        if inv_key == f'inventory_{chosen_inventory.lower()}_keys':
            continue

        voted = vote_on_record(record_string, pair)
        approvals += 1 if voted else 0

    if approvals == 3:
        store_record_to_inventories(record_string)
        return True, approvals
    else:
        return False, approvals
    

# RECORD EXAMPLES (TESTING)

# # TEST 1 - Expected Output: PASS
# test_record = "0041218A"
# result, votes = run_poa_consensus(test_record)
# print("TEST 1: Consensus successful" if result else "TEST 1: Consensus failed")

# # TEST 2 - Expected Output: PASS
# test_record = "9123891D"
# result, votes = run_poa_consensus(test_record)
# print("TEST 2: Consensus successful" if result else "TEST 2: Consensus failed")

# TEST 3 - Expected Output: FAIL — no warehouse location provided
# test_record = "0041218"
# result, votes = run_poa_consensus(test_record)
# print("TEST 3: Consensus successful" if result else "TEST 3: Consensus failed")

# # TEST 4 - Expected Output: FAIL — missing pice of data (price value not provided)
# test_record = "0041218E"
# result, votes = run_poa_consensus(test_record)
# print("TEST 4: Consensus successful" if result else "TEST 4: Consensus failed")

# # TEST 5 - Expected Output: FAIL — Invalid data (non-numeric values)
# test_record = "fj49g@$#@Y9Ggkdkg"
# result, votes = run_poa_consensus(test_record)
# print("TEST 5: Consensus successful" if result else "TEST 5: Consensus failed")