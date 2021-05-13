from flask import Flask

app = Flask(__name__)

@app.route("/")
def funcion():
    return "Flask funciona"