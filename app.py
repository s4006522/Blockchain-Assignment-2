# Starting the application with Flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib
import json
import os



app = Flask(__name__) # Set up Flask app

# # # Making the hashing algorithm for the inventory values
# hash_algorithm = 'md5' # Hash algorithm to be used

# # Opening and using json to retrieve the data
# with open('inventory_d.json', 'r') as file:
#     key_data = json.load(file)
# inventory_d_data = key_data["inventory_d"]

# # loading the private key for d  to test the signing.
# with open("d_pk_sk.json", "r") as file:
#     d_pk_sk = json.load(file)

# d_private_key = d_pk_sk["private_key"]

# d_d = d_private_key["d"]
# d_n = d_private_key["n"]



# #  hashing the inventory value of d
# hash_result = hashlib.md5(string.encode()).hexdigest()

# hash_result_decimal =int(hash_result,16)
# print(string)
# print(f"Hash result: {hash_result_decimal}")


# print("signed message")

# signed_d = pow(hash_result_decimal, d_d, d_n)

# print(signed_d)

@app.route('/') # Defining the route for the index page
def index():
    return render_template('index.html')

@app.route('/sign', methods=['POST']) # Defining the route for the sign page
def sign():
    message = request.form['message']
    selected_inventory = request.form['action']
    # checking the selected inventory based on the selected radio button, We did this beacuse we have multiple inventories
    database_file = f"{selected_inventory}_pk_sk.json"
    # Load key data from JSON
    with open(database_file, 'r') as f:
        key_data = json.load(f)
    # Accessing the keys
    public_key = key_data['public_key']
    private_key = key_data['private_key']
    # Extracting the public key values
    e = public_key['e']
    n = public_key['n']
    # Extracting the values of d and n from the private key
    d = int(private_key['d'])
    n = int(private_key['n'])

    # Hashing the message using MD5 and converting to decimal
    md5_hash_hex = hashlib.md5(message.encode()).hexdigest()
    md5_hash_decimal = int(md5_hash_hex, 16) 
    # calculating the signature using s = m^d mod n
    signature = pow(md5_hash_decimal, d, n)

    # Display everything
    return render_template(
        'signed.html',
        message=message,
        inventory=selected_inventory.upper(),
        md5_hash=md5_hash_decimal,
        signature=signature,
        private_key = d,
        public_key = n

    )


if __name__ == '__main__':
    app.run(debug=True)