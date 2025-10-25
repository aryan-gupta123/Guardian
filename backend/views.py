from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transaction, Merchant
from .serializers import TransactionSerializer, MerchantSerializer
from .services.ml.anomaly_detector import AnomalyDetector
from .services.ml.explainability import ExplainabilityService

# Homepage view
def homepage(request):
    return render(request, 'homepage.html')

# API Views
@api_view(['POST'])
def ingest_transaction(request):
    """Ingest a new transaction for analysis"""
    try:
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            
            # Score the transaction
            detector = AnomalyDetector()
            risk_score, is_anomaly = detector.score_transaction(transaction)
            
            # Update transaction with risk score
            transaction.risk_score = risk_score
            transaction.is_anomaly = is_anomaly
            transaction.save()
            
            return Response({
                'transaction_id': transaction.id,
                'risk_score': risk_score,
                'is_anomaly': is_anomaly,
                'status': 'success'
            })
        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def score_transaction(request, transaction_id):
    """Get risk score for a specific transaction"""
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        return Response({
            'transaction_id': transaction.id,
            'risk_score': transaction.risk_score,
            'is_anomaly': transaction.is_anomaly,
            'amount': transaction.amount,
            'merchant': transaction.merchant.name if transaction.merchant else None
        })
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=404)

@api_view(['GET'])
def explain_transaction(request, transaction_id):
    """Get explanation for a transaction's risk score"""
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        explainer = ExplainabilityService()
        explanation = explainer.explain_transaction(transaction)
        return Response(explanation)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=404)

@api_view(['POST'])
def agent_action(request):
    """Handle agent actions (block, allow, investigate)"""
    try:
        transaction_id = request.data.get('transaction_id')
        action = request.data.get('action')  # 'block', 'allow', 'investigate'
        
        if not transaction_id or not action:
            return Response({'error': 'Missing transaction_id or action'}, status=400)
        
        transaction = Transaction.objects.get(id=transaction_id)
        
        # Update transaction status based on action
        if action == 'block':
            transaction.status = 'blocked'
        elif action == 'allow':
            transaction.status = 'allowed'
        elif action == 'investigate':
            transaction.status = 'under_investigation'
        
        transaction.save()
        
        return Response({
            'transaction_id': transaction.id,
            'action': action,
            'status': transaction.status,
            'message': f'Transaction {action}ed successfully'
        })
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_merchant(request, merchant_id):
    """Get merchant information"""
    try:
        merchant = Merchant.objects.get(id=merchant_id)
        serializer = MerchantSerializer(merchant)
        return Response(serializer.data)
    except Merchant.DoesNotExist:
        return Response({'error': 'Merchant not found'}, status=404)

@api_view(['GET'])
def get_high_risk_transactions(request):
    """Get all high-risk transactions"""
    try:
        high_risk_transactions = Transaction.objects.filter(
            is_anomaly=True,
            status__in=['pending', 'under_investigation']
        ).order_by('-created_at')
        
        serializer = TransactionSerializer(high_risk_transactions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)