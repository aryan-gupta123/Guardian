from rest_framework import serializers
from .models import Merchant, Transaction, AgentAction, ScamDetection


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'


class AgentActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentAction
        fields = '__all__'


class ScamDetectionRequestSerializer(serializers.Serializer):
    """
    Serializer for scam detection request input.
    """
    company_name = serializers.CharField(max_length=255, required=True,
                                        help_text="Name of the company to analyze")
    domain = serializers.CharField(max_length=255, required=False, allow_blank=True,
                                  help_text="Company website domain (e.g., example.com)")
    jurisdiction = serializers.CharField(max_length=50, required=False, default='US',
                                        help_text="Company jurisdiction (e.g., US, UK)")
    company_identifier = serializers.CharField(max_length=100, required=False, allow_blank=True,
                                              help_text="CIK number or ticker symbol")
    business_description = serializers.CharField(required=False, allow_blank=True,
                                                help_text="Description of business model")
    promised_returns = serializers.FloatField(required=False,
                                             help_text="Promised annual returns percentage")
    payment_methods = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of payment methods (e.g., ['credit_card', 'cryptocurrency'])"
    )


class ScamDetectionSerializer(serializers.ModelSerializer):
    """
    Serializer for scam detection results.
    """
    class Meta:
        model = ScamDetection
        fields = [
            'id',
            'company_name',
            'domain',
            'company_identifier',
            'jurisdiction',
            'overall_risk_score',
            'risk_level',
            'category_scores',
            'red_flags',
            'green_flags',
            'detailed_findings',
            'recommendations',
            'analysis_date',
            'updated_at',
            'merchant',
        ]
        read_only_fields = ['id', 'analysis_date', 'updated_at']


class ScamDetectionListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing scam detections.
    """
    class Meta:
        model = ScamDetection
        fields = [
            'id',
            'company_name',
            'domain',
            'overall_risk_score',
            'risk_level',
            'analysis_date',
        ]

