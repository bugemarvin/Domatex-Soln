import os
import base58
from solana.rpc.api import Client
from solana.transaction import Transaction
import solana
from solana import transaction as TransactionInstruction
from dotenv import load_dotenv
import Crypto.PublicKey

# Initialize Solana client
solana_uri = os.getenv("SOLANA_URI")
client = Client(solana_uri)

# Load environment data
load_dotenv()

def create_solana_account(user):
    # Generate a new Solana account for the user
    account = solana.Account()
    user.solana_public_key = str(account.public_key())
    user.solana_private_key = str(account.secret_key())
    user.save()

def transfer_solana_tokens(sender, recipient_address, amount):
    # Transfer Solana tokens from sender to recipient checking on the confidentialiity of the key comparing the hashes
    sender_account = solana.Account(private_key=sender.solana_private_key)
    recipient_address = solana.publickey(recipient_address)

    # Create a transaction to transfer tokens
    transaction = Transaction().add(
        TransactionInstruction(
            keys=[
                {"pubkey": sender_account.public_key, "isSigner": True, "isWritable": False},
                {"pubkey": recipient_address, "isSigner": False, "isWritable": True},
            ],
            program_id=solana.publickey("Transfer111111111111111111111111111111111"),
            data=TransactionInstruction.encode_u8_array([
                amount & 0xFF,
                (amount >> 8) & 0xFF,
                (amount >> 16) & 0xFF,
                (amount >> 24) & 0xFF,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]),
        )
    )

    # Sign the transaction with the sender's private key
    transaction.sign([sender_account])

    # Send the transaction to the Solana network
    client.send_transaction(transaction)

def get_solana_token_balance(user):
    # Retrieve the Solana token balance for the user
    account_address = solana.publickey(user.solana_public_key)

    # Get the token balance for the user's account
    token_balance = client.get_token_balance(account_address)

    return token_balance

def interact_with_solana_program(program_id, public_key, input_data):
    # Connect to the Solana RPC endpoint
    client = Client(solana_uri)

    # Create a transaction to call the program
    transaction = Transaction().add(
        TransactionInstruction(
            keys=[
                {"pubkey": solana.publickey(public_key), "isSigner": False, "isWritable": True},
            ],
            program_id=solana.publickey(program_id),
            data=input_data,
        )
    )
  
    # Generate and update the public and private keys
    # Generate a new private key
    private_key = Crypto.PublicKey.Ed25519.generate()

    # Convert the private key to bytes
    private_key_bytes = private_key.to_bytes()

    # Convert the private key to a base58-encoded string
    private_key_string = base58.b58encode(private_key_bytes).decode()

    # Get the public key from the private key
    public_key = private_key.publickey()

    # Convert the public key to bytes
    public_key_bytes = public_key.to_bytes()

    # Convert the public key to a base58-encoded string
    public_key_string = base58.b58encode(public_key_bytes).decode()

    # Sign and send the transaction
    signature = client.send_transaction(transaction, [private_key])

    # Wait for the transaction to be confirmed
    client.confirm_transaction(signature)

    # Get the output data of the transaction
    transaction_response = client.get_transaction(signature)
    return transaction_response["result"]["meta"]["innerInstructions"][0]["instructions"][0]["data"]