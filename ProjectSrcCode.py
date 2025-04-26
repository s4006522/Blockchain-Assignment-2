# Task 1
# Part 1 Creating PK and SK
from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib
import json
import os

app = Flask(__name__) # Set up Flask app

@app.route('/') # Defining the route for the index page
def index():
    return render_template('index.html')

app.run(debug=True)


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

def inventory_a_record_creation():
    # Creating a record for inventory A
    message = {
        "inventory_a": {
            "item_id": "004",
            "item_qty": 12,
            "iten_price": 18,
            "location": "A"
        }
    }

    with open('inventory_a.json', 'w') as file:
        json.dump(message, file, indent=3)
inventory_a_record_creation()

def inventory_b_record_creation():
    # Creating a record for inventory A
    message = {
        "inventory_b": {
            "item_id": "004",
            "item_qty": 12,
            "iten_price": 18,
            "location": "B"
        }
    }

    with open('inventory_b.json', 'w') as file:
        json.dump(message, file, indent=3)
inventory_b_record_creation()

def inventory_c_record_creation():
    # Creating a record for inventory A
    message = {
        "inventory_c": {
            "item_id": "004",
            "item_qty": 12,
            "iten_price": 18,
            "location": "C"
        }
    }

    with open('inventory_c.json', 'w') as file:
        json.dump(message, file, indent=3)
inventory_c_record_creation()

def inventory_d_record_creation():
    # Creating a record for inventory A
    message = {
        "inventory_d": {
            "item_id": "004",
            "item_qty": 12,
            "iten_price": 18,
            "location": "D"
        }
    }

    with open('inventory_d.json', 'w') as file:
        json.dump(message, file, indent=3)
inventory_d_record_creation()