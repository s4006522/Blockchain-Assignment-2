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
    inventory = ['a','b','c','d']
    for i in inventory:
        with open(f'inventory_{i}.json', 'r') as f:
            key = json.load(f)
            key = key
    
    return render_template(
        'task3.html',
        key = key
        )
    # Get the message and signature from the form
# THIS IS  ATEST

if __name__ == '__main__':
    app.run(debug=True)