# Task 1
# Part 1 Creating PK and SK

import hashlib
import json
import os

# Opening and using json to retrieve the data
with open('list_of_keys', 'r') as file:
    key_data = json.load(file)

# Calculating PK and SK Of all inventories A/B/C/d
# Accessing Inventory a keys
key_data["inventory_a_keys"]
inventory_a_keys = key_data["inventory_a_keys"]

print(inventory_a_keys)
