from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import wallet.bitcoin_utils
from wallet.solana_utils import create_solana_account, get_solana_token_balance
from .models import Transaction
import wallet.solana_utils
# from .solana_utils import (
#     create_solana_account,
#     transfer_solana_tokens,
#     get_solana_token_balance,
#     interact_with_solana_program,
#     retrieve_solana_blockchain_data,
# )

# from .bitcoin_utils import (
#     create_bitcoin_wallet,
#     send_bitcoin_transaction,
#     get_bitcoin_balance,
#     retrieve_bitcoin_blockchain_data,
# )
from cryptography.fernet import Fernet
import os
import hashlib

@login_required
def wallet_home(request):
    # Your logic for the wallet home view
    return render(request, 'wallet/home.html')

@login_required
def create_account(request):
    # Create Solana account
    create_solana_account(request.user)

    # Create Bitcoin wallet
    wallet.bitcoin_utils.create_bitcoin_wallet(request.user)

    return redirect('wallet:home')

@login_required
def profile(request):
    # Your logic for the user profile view
    return render(request, 'wallet/profile.html')

@login_required
def transaction_history(request):
    # Retrieve transaction history
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'wallet/transaction_history.html', {'transactions': transactions})

@login_required
def token_balance(request):
    # Retrieve Solana token balance
    solana_balance = get_solana_token_balance(request.user)

    # Retrieve Bitcoin balance
    bitcoin_balance = wallet.bitcoin_utils.create_bitcoin_wallet.balance(request.user)

    return render(request, 'wallet/token_balance.html', {'solana_balance': solana_balance, 'bitcoin_balance': bitcoin_balance})

@login_required
def solana_account_creation(request):
    # Create Solana account for the user
    wallet.solana_utils.create_solana_account(request.user)
    return redirect('wallet:profile')

@login_required
def token_transfer(request):
    # Transfer Solana tokens
    if request.method == 'POST':
        recipient_address = request.POST['recipient_address']
        amount = request.POST['amount']
        wallet.solana_utils.transfer_solana_tokens(request.user, recipient_address, amount)
        return redirect('wallet:transaction_history')
    return render(request, 'wallet/token_transfer.html')

@login_required
def bitcoin_transaction(request):
    # Send Bitcoin transaction
    if request.method == 'POST':
        recipient_address = request.POST['recipient_address']
        amount = request.POST['amount']
        wallet.bitcoin_utils.send_bitcoin_transaction(request.user, recipient_address, amount)
        return redirect('wallet:transaction_history')
    return render(request, 'wallet/bitcoin_transaction.html')

@login_required
def solana_program_interaction(request):
    # Interact with Solana program
    wallet.solana_utils.interact_with_solana_program()
    return redirect('wallet:home')

@login_required
def blockchain_data_retrieval(request):
    # Retrieve data from the Solana blockchain
    solana_data = wallet.solana_utils.retrieve_solana_blockchain_data()

    # Retrieve data from the Bitcoin blockchain
    bitcoin_data = wallet.bitcoin_utils.retrieve_bitcoin_blockchain_data()

    return render(request, 'wallet/blockchain_data.html', {'solana_data': solana_data, 'bitcoin_data': bitcoin_data})

def encrypt_data(data, encryption_key):
    cipher_suite = Fernet(encryption_key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data, encryption_key):
    cipher_suite = Fernet(encryption_key)
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

def bitcoin_balance():
    wallet.solana_utils.get_solana_token_balance()
    wallet.bitcoin_utils.get_bitcoin_balance()