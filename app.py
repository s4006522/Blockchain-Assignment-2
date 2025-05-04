# Starting the application with Flask
from flask import Flask, render_template, request, redirect, url_for, flash, session


app = Flask(__name__) # Set up Flask app

@app.route('/') # Defining the route for the index page
def index():
    return render_template('index.html', method = "get")


if __name__ == '__main__':
    app.run(debug=True)