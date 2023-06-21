from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('home/', views.wallet_home, name='home'),
    path('create-account/', views.create_account, name='create_account'),
    path('profile/', views.profile, name='profile'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('token-balance/', views.token_balance, name='token_balance'),
    path('solana-account-creation/', views.solana_account_creation, name='solana_account_creation'),
    path('token-transfer/', views.token_transfer, name='token_transfer'),
    path('bitcoin-transaction/', views.bitcoin_transaction, name='bitcoin_transaction'),
    path('solana-program-interaction/', views.solana_program_interaction, name='solana_program_interaction'),
    path('blockchain-data-retrieval/', views.blockchain_data_retrieval, name='blockchain_data_retrieval'),
]
