from flask import Flask, render_template, request, send_file, flash, redirect
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app = Flask(__name__)
app.secret_key = "future_interns_secret_key"

# -----------------------
# CONSTANTS & DIRECTORIES
# -----------------------
STORAGE_FOLDER = "storage"
KEY_FILE = "key.bin"

os.makedirs(STORAGE_FOLDER, exist_ok=True)

# -----------------------
# AES KEY MANAGEMENT
# -----------------------
def load_key():
    if not os.path.exists(KEY_FILE):
        key = get_random_bytes(32)  # AES-256 key
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()

    return key


AES_KEY = load_key()


# -----------------------
# AES ENCRYPTION & DECRYPTION
# -----------------------
def encrypt_data(data):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext  # Store nonce + tag + ciphertext


def decrypt_data(enc_data):
    nonce = enc_data[:16]
    tag = enc_data[16:32]
    ciphertext = enc_data[32:]

    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


# -----------------------
# ROUTES
# -----------------------
@app.route("/")
def index():
    stored_files = [f for f in os.listdir(STORAGE_FOLDER) if f.endswith(".enc")]
    return render_template("index.html", stored_files=stored_files)


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        flash("No file selected.")
        return redirect("/")

    file = request.files["file"]
    if file.filename == "":
        flash("Invalid file.")
        return redirect("/")

    original_filename = file.filename
    encrypted_filename = original_filename + ".enc"
    encrypted_path = os.path.join(STORAGE_FOLDER, encrypted_filename)

    data = file.read()
    encrypted_data = encrypt_data(data)

    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    flash(f"File uploaded and encrypted as: {encrypted_filename}")
    return redirect("/")


@app.route("/download-encrypted", methods=["POST"])
def download_encrypted():
    filename = request.form.get("filename")
    encrypted_path = os.path.join(STORAGE_FOLDER, filename)

    if not os.path.exists(encrypted_path):
        flash("Encrypted file not found.")
        return redirect("/")

    return send_file(encrypted_path, as_attachment=True)


@app.route("/download-decrypted", methods=["POST"])
def download_decrypted():
    filename = request.form.get("filename")

    if not filename.endswith(".enc"):
        flash("Error: Use the encrypted filename ending with .enc")
        return redirect("/")

    encrypted_path = os.path.join(STORAGE_FOLDER, filename)

    if not os.path.exists(encrypted_path):
        flash("File not found.")
        return redirect("/")

    with open(encrypted_path, "rb") as f:
        enc_data = f.read()

    try:
        decrypted_bytes = decrypt_data(enc_data)
    except:
        flash("Decryption failed. Corrupted or wrong key.")
        return redirect("/")

    decrypted_filename = filename.replace(".enc", "")

    temp_path = os.path.join(STORAGE_FOLDER, decrypted_filename)
    with open(temp_path, "wb") as f:
        f.write(decrypted_bytes)

    return send_file(temp_path, as_attachment=True)


@app.route("/keys")
def keys():
    return {
        "key_file_present": os.path.exists(KEY_FILE),
        "key_path": os.path.abspath(KEY_FILE)
    }


if __name__ == "__main__":
    app.run(debug=True)
