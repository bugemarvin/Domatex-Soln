import os
import hashlib
from cryptography.fernet import Fernet
from .models import Wallet

# AES Encryption
# Implement AES encryption algorithms (e.g., using Python's cryptography library) to encrypt sensitive data, such as private keys or user credentials, before storing them in the database.
# Apply encryption/decryption logic within the appropriate views to protect data during transmission or storage.

# AES encryption and decryption functions


def encrypt_data(data, encryption_key):
    cipher_suite = Fernet(encryption_key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data


def generate_private_key():
    # Generate a new random private key
    private_key = os.urandom(32)
    return private_key


def create_bitcoin_wallet(user):
    # Retrieve the user's encryption key from the database
    encryption_key = user.encryption_key

    # Generate a new Bitcoin private key
    private_key = generate_private_key()

    # Create a Bitcoin Wallet Import Format (WIF) representation of the private key
    wif = hashlib.sha256(private_key).digest()
    wif = b"\x80" + wif + b"\x01"
    wif_checksum = hashlib.sha256(hashlib.sha256(wif).digest()).digest()[:4]
    wif += wif_checksum
    wif_base58 = base58encode(wif)

    # Encrypt the private key using the user's encryption key
    encrypted_private_key = encrypt_data(wif_base58, encryption_key)

    # Create a new Wallet object for the user
    bitcoin_wallet = Wallet.objects.create(user=user, wallet_address='', balance=0.0)

    # Store the encrypted private key in the database field of the Wallet object
    bitcoin_wallet.encrypted_private_key = encrypted_private_key
    bitcoin_wallet.save()

    # Perform additional operations as needed

    return bitcoin_wallet

# Send bitcopin_utils
def retrieve_bitcoin_blockchain_data():
    # logics
    retrieve_bitcoin_blockchain_data(UserWarning)



def base58encode(v):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    base_count = len(alphabet)
    encode = ''
    while v >= base_count:
        v, mod = divmod(v, base_count)
        encode = alphabet[mod] + encode
    if v:
        encode = alphabet[v] + encode
    return encode
