import json
import hashlib
import os
from sympy import mod_inverse

# Implementation of consensus protocol (proof-of-authority) for the Warehouse supply-chain System 

# Load key data from list_of_keys.json and generate RSA key pairs for all inventories
def generate_all_keypairs():
    with open('list_of_keys.json', 'r') as keys:
        warehouse_keys = json.load(keys)
    
    keypairs = {}
    for name, values in warehouse_keys.items():
        p = values['p']
        q = values['q']
        e = values['e']
        n = p * q
        phi = (p - 1) * (q - 1)
        d = mod_inverse(e, phi)
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
def run_poa_consensus(record_string):
    keypairs = generate_all_keypairs()
    approvals = 0

    for inv_key, pair in keypairs.items():
        voted = vote_on_record(record_string, pair)
        approvals += 1 if voted else 0

    if approvals >= 3:
        store_record_to_inventories(record_string)
        return True, approvals
    else:
        return False, approvals