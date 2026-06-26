"""Aplicación en blanco — punto de partida."""
import os

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambiar_en_produccion")


@app.route("/")
def inicio():
    return render_template("blank.html")


@app.route("/health")
def health():
    return {"ok": True}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
