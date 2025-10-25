from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Merchant, Transaction, AgentAction
from .serializers import MerchantSerializer, TransactionSerializer, AgentActionSerializer
from .services.ml.anomaly_detector import AnomalyDetector
from .services.ml.explainability import ExplainabilityService


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        merchant = self.get_object()
        transactions = merchant.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=True, methods=['get'])
    def explain(self, request, pk=None):
        transaction = self.get_object()
        explainer = ExplainabilityService()
        explanation = explainer.explain_transaction(transaction)
        return Response(explanation)


class IngestView(APIView):
    def post(self, request):
        # Handle transaction ingestion
        data = request.data
        
        # Create or get merchant
        merchant, created = Merchant.objects.get_or_create(
            name=data.get('merchant_name'),
            defaults={
                'category': data.get('merchant_category', 'unknown'),
                'location': data.get('merchant_location', 'unknown')
            }
        )
        
        # Create transaction
        transaction = Transaction.objects.create(
            merchant=merchant,
            amount=data.get('amount'),
            timestamp=data.get('timestamp'),
            user_id=data.get('user_id'),
            features=data.get('features', {})
        )
        
        # Score the transaction
        detector = AnomalyDetector()
        risk_score, is_anomaly = detector.score_transaction(transaction)
        
        transaction.risk_score = risk_score
        transaction.is_anomaly = is_anomaly
        transaction.save()
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ScoreView(APIView):
    def post(self, request):
        # Score a transaction without saving
        data = request.data
        detector = AnomalyDetector()
        
        # Create temporary transaction object for scoring
        temp_transaction = type('obj', (object,), {
            'amount': data.get('amount'),
            'features': data.get('features', {}),
            'timestamp': data.get('timestamp')
        })
        
        risk_score, is_anomaly = detector.score_transaction(temp_transaction)
        
        return Response({
            'risk_score': risk_score,
            'is_anomaly': is_anomaly
        })


class AgentActionView(APIView):
    def post(self, request):
        # Handle agent actions
        data = request.data
        transaction_id = data.get('transaction_id')
        transaction = get_object_or_404(Transaction, id=transaction_id)
        
        action = AgentAction.objects.create(
            transaction=transaction,
            action_type=data.get('action_type'),
            reason=data.get('reason'),
            confidence=data.get('confidence', 0.0)
        )
        
        serializer = AgentActionSerializer(action)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

