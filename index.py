from flask import Flask
from .server import main

app = Flask(__name__)

@app.route('/')
def helloWorld():
    
    return "<h1>Hello world</h1>"

app.run()
