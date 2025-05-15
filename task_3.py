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

    inventory = ['a','b','c','d']
    for i in inventory:
        file = f"inventory_{i}.json"
        key = f"inventory_{i}"
    
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                inventory_data = data.get(key, {})

                for idx, record in inventory_data.items():
                    record_id = record[:3]  # Get only the first 3 characters
                    if record_id == search_query:
                        result[i.upper()] = record
        except FileNotFoundError:
            flash(f"File {file} not found.", "error")
            continue

    return render_template("task3.html", search_query=search_query, results=result)
    # Get the message and signature from the form
# THIS IS  ATEST

if __name__ == '__main__':
    app.run(debug=True)