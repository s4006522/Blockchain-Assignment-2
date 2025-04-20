# Task 1
# Part 1 Creating PK and SK

import hashlib
import json
import os

# # Opening and using json to retrieve the data
# with open('list_of_keys.json', 'r') as file:
#     key_data = json.load(file)

# # Calculating PK and SK Of all inventories A/B/C/d
# # Accessing Inventory a keys
# key_data["inventory_a_keys"]
# inventory_a_keys = key_data["inventory_a_keys"]

# # saving the p,q and e values in variables
# a_p = inventory_a_keys["p"]
# a_q = inventory_a_keys["q"]
# a_e = inventory_a_keys["e"]

# # Calculating all the required values using correct Formulas
# # a_n = a_p * a_q
# a_n = a_p * a_q

# # a_phi = (a_p - 1) * (a_q - 1)
# a_phi = (a_p - 1) * (a_q - 1)

# # a_d = a_e^-1 mod a_phi
# a_d = pow(a_e, -1, a_phi)
# print(f"Inventory A: n = {a_n}, phi = {a_phi}, d = {a_d}")

# # Storing PK and SK in json files
# a_pk_sk = {
#     "public_key": {
#         "e": a_e,
#         "n": a_n
#     },
#     "private_key": {
#         "d": a_d,
#         "n": a_n
#     }
# }

# with open('a_pk_sk.json', 'w') as file:
#     json.dump(a_pk_sk, file, indent=3)

# signing each message 
