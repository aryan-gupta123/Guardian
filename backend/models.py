from django.db import models
from django.contrib.auth.models import User


class Merchant(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    risk_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    user_id = models.CharField(max_length=100)
    risk_score = models.FloatField(default=0.0)
    is_anomaly = models.BooleanField(default=False)
    features = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.merchant.name} - ${self.amount}"


class AgentAction(models.Model):
    ACTION_TYPES = [
        ('block', 'Block Transaction'),
        ('flag', 'Flag for Review'),
        ('approve', 'Approve Transaction'),
        ('investigate', 'Investigate Further'),
    ]
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='agent_actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    reason = models.TextField()
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} - {self.transaction}"

