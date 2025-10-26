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


class ScamDetection(models.Model):
    """
    Stores results of financial scam detection analysis.
    """
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
        ('unknown', 'Unknown'),
    ]

    # Company identification
    company_name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, null=True, blank=True)
    company_identifier = models.CharField(max_length=100, null=True, blank=True, help_text="CIK or ticker symbol")
    jurisdiction = models.CharField(max_length=50, default='US')

    # Analysis results
    overall_risk_score = models.FloatField(default=0.0, help_text="Overall risk score (0-1)")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='unknown')

    # Detailed category scores
    category_scores = models.JSONField(default=dict, help_text="Risk scores by category")

    # Flags and findings
    red_flags = models.JSONField(default=list, help_text="List of red flags identified")
    green_flags = models.JSONField(default=list, help_text="List of positive indicators")
    detailed_findings = models.JSONField(default=dict, help_text="Detailed findings by category")
    recommendations = models.JSONField(default=list, help_text="Recommended actions")

    # Metadata
    analysis_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional link to merchant or transaction
    merchant = models.ForeignKey(Merchant, on_delete=models.SET_NULL, null=True, blank=True, related_name='scam_detections')

    class Meta:
        ordering = ['-analysis_date']
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['-analysis_date']),
        ]

    def __str__(self):
        return f"Scam Detection: {self.company_name} - {self.risk_level} ({self.overall_risk_score})"

