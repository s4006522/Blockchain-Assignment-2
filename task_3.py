# Starting the application with Flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib
import json
import re

app = Flask(__name__) # Set up Flask app


@app.route('/') # Defining the route for the index page
def index():
    return render_template('index2.html')

@app.route('/task3', methods=['POST']) # Defining the route for the verify page
def task3():
    search_query = request.form["search_query"]
    # Using regex to find the exact id in the search query.
    search_match = re.search(r'\b\d{3}\b', search_query)
    # If item id is not found in the search it will render a page saying Item id not found.
    if not search_match:
        return render_template('notfound.html', message = "Item ID not found"),400

    found_id = search_match.group()
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

            # checking if the id was found
            id_found = False
            # for loop to go over every item and see if record matches the item
            for record_id, record_value in inventory_data.items():
                if record_value[:3] == found_id:
                    quantity = record_value[3:5]
                    result[inv.upper()] = quantity
                    matched_record = record_value
                    matched_warehouse = record_value[-1]
                    id_found = True
                    break
            # if the item is found then it initiates the if statement and calculates all the required parts
            # for the multisignature.
            if id_found:
                Id_of_inv = int(keys["id_of_inventories"][inv])
                r = int(keys["random_inventory_number"][inv])

                g_i = pow(Id_of_inv, pkg_d, pkg_n)
                t_i = pow(r, pkg["e"], pkg_n)

                t_aggregate = (t_aggregate * t_i) % pkg_n
                # At the end of each calculation it adds the results to the partial sigs
                # so that it can be used at a later date to verify the signatures.
                partial_sigs.append({
                    "g_i": g_i,
                    "r_i": r,
                    "t_i": t_i,
                    "id" : Id_of_inv
                })
                        
        except FileNotFoundError:
            flash(f"File {file} not found.", "error")
            continue
    if not result:
     return render_template("notfound.html")
    
    if result:
        item_qty = next(iter(result.values()))

        # Consensus To validate all parties obtaining the correct same signature.
        # Adding the t_aggregate and search query into one message to hash and send to user who requested it
        hash_input = f"{t_aggregate}{item_qty}"
        hashed_message = hashlib.md5(hash_input.encode()).hexdigest()
        # converting to decimal
        hashed_message_decimal = int(hashed_message, 16)

        # Step: Compute s_j for each inventory
        s_values = []
        for sig in partial_sigs:
            g_i = sig["g_i"]
            r_i = sig["r_i"]
            # maiking it easier to calculate s_j by already calculating the second half of the message.
            ri_exp = pow(r_i, hashed_message_decimal, pkg_n)
            # Calculating each signed message.
            s_i = (g_i * ri_exp) % pkg_n
            s_values.append(s_i)

        # Now calculating the aggregate of the signed message
        s = 1 # This is here to make sure that when calculating aggregate of s it doesnt include an error
        for sj in s_values:
            s = (s * sj) % pkg_n

        # After everything is calulated (t, s, message)
        # time to do the verification which after we can send to the user.
        verification_1 = pow(s, pkg["e"], pkg_n)

        # Verification Right:
        i = 1
        for sig in partial_sigs:
            i = (i * sig["id"]) % pkg_n

        t_power = pow(t_aggregate, hashed_message_decimal, pkg_n)
        verification_2 = (i * t_power) % pkg_n

        signature_valid = False
            
        # making sure both verifications match if they do then signature valid is true.
        if verification_1 == verification_2:
            signature_valid = True
            # after the signature is verified sending the encrypted values
            # this is encrypted using the officers key
            encrypted_message = pow(int(item_qty), officer['e'], officer_n)

            decrypted_message = pow(encrypted_message, officer_priv[0], officer_priv[1])


        return render_template("task3.html", 
                               search_query=search_query, 
                               results=result,
                               partial_sigs=partial_sigs,
                               aggregated_signature=t_aggregate,
                               ID = Id_of_inv,
                               r = r,
                               g_i = g_i,
                               t_i = t_i,
                               pkg_n = pkg_n,
                               pkg_phi_n = pkg_phi_n,
                               pkg_d = pkg_d,
                               pkg = pkg,
                               matched_record = matched_record,
                               matched_warehouse = matched_warehouse,
                               signature_valid = signature_valid,
                               hashed_message = hashed_message,
                               hashed_message_decimal = hashed_message_decimal,
                               s_j = s_i,
                               s_values = s_values,
                               s = s,
                               verification_1 = verification_1,
                               verification_2 = verification_2,
                               item_qty = item_qty,
                               hash = hash_input,
                               encrypted_message = encrypted_message,
                               decrypted_message = decrypted_message)
    # Get the message and signature from the form
    # THIS IS  ATEST

if __name__ == '__main__':
    app.run(debug=True)