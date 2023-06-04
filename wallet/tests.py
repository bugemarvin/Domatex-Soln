import unittest
import sys
from django.test import TestCase
from django.contrib.auth.models import User
from wallet.models import Wallet, Transaction
import uuid


class WalletModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.wallet = Wallet.objects.create(
            user=self.user,
            wallet_address='example_address',
            balance=100.00
        )

    def test_wallet_model(self):
        self.assertEqual(str(self.wallet), self.wallet.wallet_address)
        self.assertIsInstance(self.wallet.wallet_id, uuid.UUID)
        self.assertEqual(self.wallet.user, self.user)
        self.assertEqual(self.wallet.balance, 100.00)

    def test_wallet_creation_date(self):
        self.assertIsNotNone(self.wallet.creation_date)

    def test_wallet_last_updated(self):
        self.assertIsNotNone(self.wallet.last_updated)


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.sender_wallet = Wallet.objects.create(
            user=self.user,
            wallet_address='sender_address',
            balance=100.00
        )
        self.recipient_wallet = Wallet.objects.create(
            user=self.user,
            wallet_address='recipient_address',
            balance=0.00
        )
        self.transaction = Transaction.objects.create(
            sender=self.sender_wallet,
            recipient=self.recipient_wallet,
            amount=50.00,
            fee=1.00,
            memo='Test transaction',
            confirmation_count=0,
            status='pending',
            transaction_hash='example_hash'
        )

    def test_transaction_model(self):
        self.assertEqual(str(self.transaction), str(self.transaction.transaction_id))
        self.assertEqual(self.transaction.sender, self.sender_wallet)
        self.assertEqual(self.transaction.recipient, self.recipient_wallet)
        self.assertEqual(self.transaction.amount, 50.00)
        self.assertEqual(self.transaction.fee, 1.00)
        self.assertEqual(self.transaction.memo, 'Test transaction')
        self.assertEqual(self.transaction.confirmation_count, 0)
        self.assertEqual(self.transaction.status, 'pending')
        self.assertEqual(self.transaction.transaction_hash, 'example_hash')

    def test_transaction_timestamp(self):
        self.assertIsNotNone(self.transaction.timestamp)


# Run the tests
result = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromModule(sys.modules[__name__]))
for failure in result.failures:
    print(failure[0])
print('-' * 30)
for error in result.errors:
    print(error[0])
