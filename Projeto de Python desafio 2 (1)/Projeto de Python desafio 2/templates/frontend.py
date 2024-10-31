from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/pontos")
def exibir_pontos():
    response = requests.get("http://localhost:8000/pontos/")
    pontos = response.json()
    return render_template("pontos.html", pontos=pontos)

if __name__ == "__main__":
    app.run(port=5000)