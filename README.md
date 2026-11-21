# 🔐 Secure File Encryption and Decryption

A Python-based command-line application that securely encrypts and decrypts files using **AES-256-GCM** authenticated encryption and **PBKDF2-HMAC-SHA256** password-based key derivation.

The application protects files using password-derived encryption keys, randomly generated salts and nonces, and authentication-based integrity verification.

## 📌 Project Overview

Secure File Encryption is a lightweight cryptographic tool designed to protect sensitive files from unauthorized access.

Users can encrypt files with a password and later decrypt them using the same password. The application verifies file integrity during decryption and rejects files that have been modified or encrypted with an incorrect password.

## ✨ Features

- **AES-256-GCM Encryption:** Uses authenticated symmetric encryption to protect file contents.
- **PBKDF2 Key Derivation:** Derives a 256-bit encryption key from the user's password.
- **SHA-256 Hashing:** Uses HMAC-SHA256 as the PBKDF2 pseudorandom function.
- **Random Salt Generation:** Generates a unique 16-byte salt for each encryption operation.
- **Random Nonce Generation:** Uses a randomly generated 12-byte nonce for AES-GCM.
- **Authentication Verification:** Detects unauthorized modifications to encrypted files.
- **Secure Password Input:** Uses Python's `getpass` module to prevent passwords from being displayed in the terminal.
- **Error Handling:** Handles missing files, invalid encrypted files, incorrect passwords, and integrity verification failures.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Cryptography Library | Cryptographic operations |
| AES-256-GCM | Authenticated file encryption |
| PBKDF2-HMAC-SHA256 | Password-based key derivation |
| SHA-256 | Cryptographic hash function |
| Argparse | Command-line argument handling |
| Getpass | Hidden password input |

## 📂 Project Structure

```text
Secure-File-Encryption/
│
├── secure_file_tool.py
│
├── README.md
│
├── requirements.txt
│
├── .gitignore
│
├── LICENSE
│
├── screenshots/
│
└── tests/
    └── test_encryption.py
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Secure-File-Encryption.git
```

### 2. Navigate to the Project Directory

```bash
cd Secure-File-Encryption
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Usage

The application supports two operations:

1. File Encryption
2. File Decryption

### 🔒 Encrypt a File

Run the following command:

```bash
python secure_file_tool.py encrypt input.pdf encrypted.enc
```

You will be prompted to enter a password.

The application will encrypt the specified file and save the encrypted output as `encrypted.enc`.

### 🔓 Decrypt a File

Run:

```bash
python secure_file_tool.py decrypt encrypted.enc decrypted.pdf
```

Enter the same password used during encryption.

If authentication succeeds, the original file contents will be restored and saved as `decrypted.pdf`.

### Example

**Encryption:**

```text
Enter password:
[+] Successfully encrypted 'input.pdf' to 'encrypted.enc'
```

**Decryption:**

```text
Enter password:
[+] Successfully decrypted 'encrypted.enc' to 'decrypted.pdf'
```

**Incorrect Password:**

```text
Enter password:
[-] Decryption failed: Incorrect password or file has been tampered with.
```

## 🔬 Encryption Workflow

The application follows this cryptographic workflow:

```text
                 ORIGINAL FILE
                       |
                       v
              Generate Random Salt
                  (16 Bytes)
                       |
                       v
             Generate Random Nonce
                  (12 Bytes)
                       |
                       v
              PBKDF2-HMAC-SHA256
                Key Derivation
                       |
                       v
              Generate AES-256 Key
                 (256 Bits)
                       |
                       v
                AES-256-GCM
                   Encryption
                       |
                       v
              Encrypted File Output
```

## 🔑 Cryptographic Configuration

The implementation uses the following cryptographic parameters:

| Parameter | Configuration |
|---|---|
| Encryption Algorithm | AES-256-GCM |
| Key Size | 256 bits |
| Key Derivation | PBKDF2 |
| Hash Algorithm | SHA-256 |
| PBKDF2 Iterations | 600,000 |
| Salt Size | 16 bytes |
| Nonce Size | 12 bytes |
| Authentication Tag | 16 bytes |

## 📦 Encrypted File Structure

The encrypted output is stored in binary format using the following structure:

```text
+--------------------+
|     Salt (16 B)    |
+--------------------+
|    Nonce (12 B)    |
+--------------------+
|                    |
|     Ciphertext     |
|                    |
+--------------------+
| Authentication Tag |
|       (16 B)       |
+--------------------+
```

The authentication tag is automatically appended to the ciphertext by the AES-GCM implementation.

The salt and nonce are stored alongside the encrypted data because they are required during decryption. They are not secret encryption keys.

## 🛡️ Security Considerations

- Passwords are entered through a hidden terminal prompt.
- Encryption keys are derived from passwords using PBKDF2-HMAC-SHA256.
- A new random salt and nonce are generated for each encryption operation.
- AES-GCM provides confidentiality and authentication.
- Modified encrypted files fail authentication verification.
- Incorrect passwords prevent successful decryption.
- Passwords are not stored by the application.

**Important:** The security of encrypted files depends partly on the strength and secrecy of the password. Use a strong, unique password.

Losing the encryption password means that the application cannot recover the original file.

## ⚠️ Current Limitations

- The application reads the entire file into memory before encryption or decryption. Very large files may require substantial memory.
- The application does not provide password recovery.
- The application does not currently support streaming encryption.
- Password strength validation is not implemented.
- The application does not preserve original file metadata.
- The application does not prevent overwriting an existing output file.

Do not overwrite your original files until you have verified that encryption and decryption work correctly.

## 🧪 Testing

The application should be tested against the following scenarios:

| Test Case | Expected Result |
|---|---|
| Encrypt a valid file | Encryption succeeds |
| Decrypt an encrypted file | Original contents are restored |
| Enter an incorrect password | Decryption fails |
| Modify encrypted data | Authentication fails |
| Provide a nonexistent file | Appropriate error message |
| Provide an invalid encrypted file | Appropriate error message |

## 🎯 Project Objectives

- Understand practical applications of symmetric encryption.
- Implement password-based cryptographic key derivation.
- Explore authenticated encryption using AES-GCM.
- Understand salt and nonce generation.
- Implement file integrity verification.
- Apply cryptographic concepts to a practical cybersecurity application.

## 👨‍💻 Author

**Mohamed Abdullah R**

GitHub: https://github.com/Mohackmed

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

⭐ If you find this project useful, consider giving the repository a star!
