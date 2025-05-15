# Starting the application with Flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib
import json
import os

app = Flask(__name__) # Set up Flask app


@app.route('/') # Defining the route for the index page
def index():
    return render_template('index2.html')

@app.route('/task3', methods=['POST']) # Defining the route for the verify page
def task3():
    search_query = request.form["search_query"]
    result = {}
    partial_sigs =[]
    t_aggregate = 1 # Initialize t_aggregate to 1 to ensure correct multiplication later on

    #load keys from list_of_keys.json
    with open("list_of_keys.json", "r") as f:
        keys = json.load(f)

    # generate PKG key pair
        pkg = keys["pkg"]
        pkg_n = pkg["p"] * pkg["q"]
        pkg_phi_n = (pkg["p"] - 1) * (pkg["q"] - 1)
        pkg_d = pow(pkg["e"], -1, pkg_phi_n)

    # public and private key for PKG
        pkg_pub = (pkg["e"], pkg_n)
        pkg_priv = (pkg_d, pkg_n)

    # procurement officer key pair (for verification)
        officer = keys["procurment_officer"]
        officer_n = officer["p"] * officer["q"]
        officer_phi = (officer["p"] - 1) * (officer["q"] - 1)
        officer_d = pow(officer["e"], -1, officer_phi)

    # public and private key for procurement officer
        officer_pub = (officer["e"], officer_n)
        officer_priv = (officer_d, officer_n)
    
    # list of inventories
    inventory = ['a','b','c','d'] 

    for inv in inventory:
        file = f"inventory_{inv}.json"
        key = f"inventory_{inv}"
    
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                inventory_data = data.get(key, {})

                for idx, record in inventory_data.items():
                    if record[:3] == search_query:
                        result[inv.upper()] = record

                        ID = keys["id_of_inventories"][inv]
                        r = keys["random_inventory_number"][inv]

                        g_i = pow(ID, pkg_d, pkg_n)
                        t_i = pow(r, pkg["e"], pkg_n)

                        t_aggregate = (t_aggregate * t_i) % pkg_n
                       
                       #append the partial signature
                        partial_sigs.append({
                            "g_i": g_i,
                            "r_i": r,
                            "t_i": t_i
                        })
                        
        except FileNotFoundError:
            flash(f"File {file} not found.", "error")
            continue

        # Encrypt/decrypt T using procurement officer's keys (consensus process)
        encrypted_t_aggregate = pow(t_aggregate, officer["e"], officer_n)
        decrypted_t_aggregate = pow(encrypted_t_aggregate, officer_d, officer_n)

        # Check if consensus is valid
        is_valid = (decrypted_t_aggregate == t_aggregate)

    return render_template("task3.html", 
                           search_query=search_query, 
                           results=result,
                           partial_sigs=partial_sigs,
                           aggregated_signature=t_aggregate,
                           encrypted_signature=encrypted_t_aggregate,
                           decrypted_signature=decrypted_t_aggregate,
                           is_valid=is_valid)
    # Get the message and signature from the form
# THIS IS  ATEST

if __name__ == '__main__':
    app.run(debug=True)