# Starting the application with Flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
from poa_consensus import run_poa_consensus 
import hashlib
import json
import os



app = Flask(__name__) # Set up Flask app


@app.route('/') # Defining the route for the index page
def index():
    return render_template('index.html')

@app.route('/sign', methods=['POST']) # Defining the route for the sign page
def sign():
    message = request.form['message']
    selected_inventory = request.form['action']
    # checking the selected inventory based on the selected radio button, We did this beacuse we have multiple inventories
    list_of_keys = "list_of_keys.json"
    # Load key data from JSON
    with open(list_of_keys, 'r') as f:
        key_data = json.load(f)
    
    # # Accessing the keys depending on the inventory selected
    p = key_data[f'inventory_{selected_inventory}_keys']['p']
    q = key_data[f'inventory_{selected_inventory}_keys']['q']
    e = key_data[f'inventory_{selected_inventory}_keys']['e']

    # # Calculating n
    n = p * q
    
    # # Calculating phi
    phi = (p - 1) * (q - 1)
    
    # # Calculating d
    d = pow(e, -1, phi)

    # # After Private key is calculated, we can now sign the message
    # Hashing the message using MD5 and converting to decimal
    md5_hash_hex = hashlib.md5(message.encode()).hexdigest()
    md5_hash_decimal = int(md5_hash_hex, 16) 
    # calculating the signature using s = m^d mod n
    signature = pow(md5_hash_decimal, d, n)
    inv_output = message + selected_inventory.upper()
    accepted, votes = run_poa_consensus(inv_output)

    # Display everything
    return render_template(
        'signed.html',
        message=message,
        inventory=selected_inventory.upper(),
        md5_hash=md5_hash_decimal,
        signature=signature,
        private_key = d,
        public_key = n,
        accepted=accepted,
        votes=votes

    )
@app.route('/task3', methods=['POST']) # Defining the route for the verify page
def task3():
    return render_template('task3.html')
    # Get the message and signature from the form


if __name__ == '__main__':
    app.run(debug=True)