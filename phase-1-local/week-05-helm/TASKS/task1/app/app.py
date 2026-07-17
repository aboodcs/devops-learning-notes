from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "Flask Helm App")
APP_ENV = os.getenv("APP_ENV", "dev")


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Flask deployed with Helm!",
        "app": APP_NAME,
        "environment": APP_ENV
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/info")
def info():
    return jsonify({
        "app": APP_NAME,
        "environment": APP_ENV,
        "hostname": socket.gethostname()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
