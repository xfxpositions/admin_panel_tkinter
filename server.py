from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import os
from utils.secretsmanager import SecretsManager

app = Flask(__name__)
secrets_manager = SecretsManager()


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


@app.route("/add_openai_config", methods=["POST"])
def add_openai_config():
    content = request.json
    try:
        new_config = OpenAIConfig(
            name=content["name"],
            apiKey=content["apiKey"],
            url=content["url"],
            embeddingKey=content["embeddingKey"],
            searchKey=content["searchKey"],
            indexname=content["indexname"],
        )
        secrets_manager.add_openai_config(new_config)
        return jsonify({"message": "OpenAI configuration added successfully"})
    except KeyError as e:
        return jsonify({"error": "Missing parameter", "parameter": str(e)}), 400


@app.route("/get_configs", methods=["GET"])
def get_configs():
    configs = [vars(config) for config in secrets_manager.openai_configs]
    return jsonify(configs)


@app.route("/edit_openai_config", methods=["POST"])
def edit_openai_config():
    content = request.json
    config_index = content.get("config_index")
    if config_index is None:
        return jsonify({"error": "Config index is required"}), 400
    try:
        selected_config = secrets_manager.openai_configs[config_index]
        for key, value in content.items():
            if hasattr(selected_config, key):
                setattr(selected_config, key, value)
        secrets_manager.to_json(secrets_manager.settings_filename)
        return jsonify({"message": "Configuration updated successfully"})
    except IndexError:
        return jsonify({"error": "Invalid configuration index"}), 400
    except Exception as e:
        return (
            jsonify({"error": "Failed to update configuration", "message": str(e)}),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, port=9000)
