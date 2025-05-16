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

                for record, value in inventory_data.items():

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
                    if value[:3] == search_query:
                            result = value[3:5]
                        
        except FileNotFoundError:
            flash(f"File {file} not found.", "error")
            continue


    if result:
        # Consensus To validate all parties obtaining the correct same signature.
        # Adding the t_aggregate and search query into one message to hash and send to user who requested it
        hashed_message = hashlib.md5((str(t_aggregate) + result).encode()).hexdigest()
        # converting to decimal
        hashed_message_decimal = int(hashed_message, 16)
        # Step: Compute s_j for each inventory
        s_values = []
        for sig in partial_sigs:
            g_j = sig["g_i"]
            r_j = sig["r_i"]
            # maiking it easier to calculate s_j by already calculating the second half of the message.
            rj_exp = pow(r_j, hashed_message_decimal, pkg_n)
            # Calculating each signed message.
            s_j = (g_j * rj_exp) % pkg_n
            s_values.append(s_j)

        # Now calculating the aggregate of the signed message
        s = 1 # This is here to make sure that when calculating aggregate of s it doesnt include an error
        for sj in s_values:
            s = (s * sj) % pkg_n

        # After everything is calulated (t, s, message)
        # time to do the verification which after we can send to the user.
        verification_1 = pow(s, pkg["e"], pkg_n)

        # Verification Right:
        g_product = 1
        for sig in partial_sigs:
            g_product = (g_product * sig["g_i"]) % pkg_n

        t_power = pow(t_aggregate, hashed_message_decimal, pkg_n)
        verification_2 = (g_product * t_power) % pkg_n

        signature_valid = False

        if verification_1 == verification_2:
            signature_valid = True
        else:
            signature_valid = False            

    else:
        message = None
  


    return render_template("task3.html", 
                           search_query=search_query, 
                           results=result,
                           partial_sigs=partial_sigs,
                           aggregated_signature=t_aggregate,
                           ID = ID,
                           r = r,
                           g_i = g_i,
                           t_i = t_i,
                           pkg_n = pkg_n,
                           pkg_phi_n = pkg_phi_n,
                           pkg_d = pkg_d,
                           pkg = pkg,
                           signature_valid = signature_valid,
                           hashed_message = hashed_message,
                           s_j = s_j,
                           s = s,
                           verification_1 = verification_1,
                           verification_2 = verification_2)
    # Get the message and signature from the form
# THIS IS  ATEST

if __name__ == '__main__':
    app.run(debug=True)