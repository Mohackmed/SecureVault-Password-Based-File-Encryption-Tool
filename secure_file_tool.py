import os
import sys
import argparse
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

# --- Cryptographic Constants ---
SALT_SIZE = 16
NONCE_SIZE = 12
ITERATIONS = 600_000  # OWASP recommended minimum for PBKDF2-HMAC-SHA256

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a 256-bit AES key from a password and a salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 bytes = 256 bits
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_file(input_path: str, output_path: str, password: str):
    """Encrypts a file securely using AES-256-GCM."""
    try:
        with open(input_path, 'rb') as f:
            plaintext = f.read()
    except FileNotFoundError:
        print(f"[-] Error: File '{input_path}' not found.")
        return

    # 1. Generate secure random salt and nonce
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    # 2. Derive key and initialize AES-GCM
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    # 3. Encrypt data (The auth tag is automatically appended by AESGCM)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    # 4. Write Salt + Nonce + Ciphertext to the new file
    with open(output_path, 'wb') as f:
        f.write(salt + nonce + ciphertext)
    
    print(f"[+] Successfully encrypted '{input_path}' to '{output_path}'")

def decrypt_file(input_path: str, output_path: str, password: str):
    """Decrypts a file and verifies its integrity."""
    try:
        with open(input_path, 'rb') as f:
            file_data = f.read()
    except FileNotFoundError:
        print(f"[-] Error: File '{input_path}' not found.")
        return

    # Ensure file is large enough to contain at least salt, nonce, and a 16-byte tag
    if len(file_data) < (SALT_SIZE + NONCE_SIZE + 16):
        print("[-] Error: File is too small to be a valid encrypted file.")
        return

    # 1. Extract Salt, Nonce, and Ciphertext
    salt = file_data[:SALT_SIZE]
    nonce = file_data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = file_data[SALT_SIZE + NONCE_SIZE:]

    # 2. Derive the original key
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    # 3. Decrypt and verify integrity
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    except InvalidTag:
        print("[-] Decryption failed: Incorrect password or file has been tampered with.")
        return

    # 4. Write the original plaintext to disk
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    
    print(f"[+] Successfully decrypted '{input_path}' to '{output_path}'")

def main():
    parser = argparse.ArgumentParser(description="Secure File Encrypter/Decrypter (AES-256-GCM)")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Action to perform")
    parser.add_argument("input_file", help="Path to the target file")
    parser.add_argument("output_file", help="Path to save the resulting file")
    
    args = parser.parse_args()
    
    # Prompt for password securely without echoing it to the terminal
    import getpass
    password = getpass.getpass("Enter password: ")

    if args.mode == "encrypt":
        encrypt_file(args.input_file, args.output_file, password)
    elif args.mode == "decrypt":
        decrypt_file(args.input_file, args.output_file, password)

if __name__ == "__main__":
    main()