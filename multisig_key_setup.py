import json
import hashlib
import os

#load keys from list_of_keys.json
with open("list_of_keys.json", "r") as f:
    keys = json.load(f)

# Generate PKG key pair
pkg = keys["pkg"]
pkg_n = pkg["p"] * pkg["q"]
pkg_phi_n = (pkg["p"] - 1) * (pkg["q"] - 1)
pkg_d = pow(pkg["e"], -1, pkg_phi_n)

# public and private key for PKG
pkg_pub = (pkg["e"], pkg_n)
pkg_priv = (pkg_d, pkg_n)

# retrive id for each inventory
identity_id = keys["id_of_inventories"]

# Compute secret key for inventories
for inv in ['a', 'b', 'c', 'd']:
    id = identity_id[inv]
    g_i = pow(id, pkg_d, pkg_n)
    var_name = f"g_{inv}"


# # TEST : check if PKG key pair is correct
#     print(f" PKG Public Key: {pkg_pub}")
#     print(f"PKG Private Key: {pkg_priv}")


# # TEST : check if g_i output is correct
#     print(f"{var_name} = {g_i}")