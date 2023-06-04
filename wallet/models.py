from django.db import models
from django.contrib.auth.models import User
import uuid

class Wallet(models.Model):
    wallet_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=256)
    balance = models.DecimalField(max_digits=20, decimal_places=8)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wallet_address}"


class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(Wallet, related_name='sent_transactions', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Wallet, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    fee = models.DecimalField(max_digits=20, decimal_places=8)
    memo = models.CharField(max_length=256)
    confirmation_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    transaction_hash = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.transaction_id}"
