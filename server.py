from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import os

app = Flask(__name__)


class CryptoManager:
    def __init__(self, key_file="secret.key"):
        self.key_file = key_file
        self.key = self.load_or_generate_key()

    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                return key_file.read()
        else:
            return self.generate_key()

    def generate_key(self):
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)
        return key

    def encrypt_message(self, message):
        f = Fernet(self.key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message.decode()

    def decrypt_message(self, encrypted_message):
        f = Fernet(self.key)
        decrypted_message = f.decrypt(encrypted_message.encode())
        return decrypted_message.decode()


crypto_manager = CryptoManager()


@app.route("/encrypt", methods=["POST"])
def encrypt():
    message = request.json.get("message")
    if message:
        encrypted_message = crypto_manager.encrypt_message(message)
        return jsonify({"encrypted": encrypted_message})
    else:
        return jsonify({"error": "No message provided"}), 400


@app.route("/decrypt", methods=["POST"])
def decrypt():
    encrypted_message = request.json.get("encrypted_message")
    if encrypted_message:
        try:
            decrypted_message = crypto_manager.decrypt_message(encrypted_message)
            return jsonify({"decrypted": decrypted_message})
        except Exception as e:
            return jsonify({"error": "Decryption failed", "message": str(e)}), 400
    else:
        return jsonify({"error": "No encrypted message provided"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=9000)
