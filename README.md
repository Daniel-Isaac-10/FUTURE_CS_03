 FUTURE_CS_03

🔐 Secure File Sharing System (AES Encrypted)

Cyber Security Internship – Task 3 (Future Interns)
Built by: Daniel Isaac E

📌 Project Overview

This project is a secure file upload & download system built using Python Flask with built-in AES-256 encryption.
All uploaded files are encrypted before storage, ensuring strong data confidentiality.

This simulates how real companies implement secure document exchange portals.

🚀 Features
✔ Upload files securely (AES-256 encryption)
✔ Download encrypted files (.enc)
✔ Download decrypted original files
✔ Clean, modern UI
✔ Safe key management
✔ No plaintext stored on server
🛠️ Tech Stack

Python Flask – backend

PyCryptodome – AES encryption

HTML + CSS – UI

Local file storage

GitHub – version control

📂 Project Structure
secure-file-share/
│── app.py
│── key.key
│── storage/
│── templates/
│   └── index.html
│── static/ (optional)
└── README.md

🔧 How to Run the Project
1. Install dependencies
pip install flask pycryptodome

2. Run the application
python app.py

3. Open in browser
http://127.0.0.1:5000

📸 Screenshots Included

The repo includes:

Homepage UI

Upload success

Encrypted file stored

Download encrypted

Download decrypted

Key management

GitHub repo layout

🔐 Security Notes

Uses AES-256 in CBC mode

Key stored securely in key.key

No plaintext files saved

Safe filename handling

Decryption only on request

📘 Documentation

A full report (PDF/Word) is provided, covering:

Architecture

Encryption workflow

Screenshots

Security considerations

👨‍💻 Author

Daniel Isaac E
Cyber Security Student & Future Interns Trainee

📄 License

This project is for internship/educational use.
