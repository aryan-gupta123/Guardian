from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transaction, Merchant, ScamDetection
from .serializers import (
    TransactionSerializer, MerchantSerializer,
    ScamDetectionRequestSerializer, ScamDetectionSerializer,
    ScamDetectionListSerializer
)
from .services.ml.anomaly_detector import AnomalyDetector
from .services.ml.explainability import ExplainabilityService
from .services.scraping.scam_detector import FinancialScamDetector
from anomaly_detection.ml.scorer import SCORER
from anomaly_detection.ml.bootstrap import bootstrap_fit

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

@api_view(['POST'])
def ml_score_transaction(request):
    """Score a transaction using the full ML model"""
    try:
        # Bootstrap the model if not already fitted
        if not SCORER._fitted:
            bootstrap_fit(SCORER)

        # Extract transaction data from request
        transaction_data = request.data

        # Prepare features for ML model
        features = {
            "amount": transaction_data.get('amount', 0.0),
            "hour": transaction_data.get('hour', 12),
            "is_foreign": 1.0 if transaction_data.get('is_foreign', False) else 0.0,
            "merchant_risk": transaction_data.get('merchant_risk', 0.0),
            "user_txn_rate": transaction_data.get('user_txn_rate', 0.0)
        }

        # Create transaction object for ML scoring
        txn = {
            "id": transaction_data.get('id', 'txn_001'),
            "features": features
        }

        # Score the transaction
        result = SCORER.score_batch([txn])

        if result:
            score_data = result[0]
            return Response({
                'transaction_id': score_data['id'],
                'risk_score': score_data['score'],
                'reasons': score_data['reasons'],
                'status': 'success'
            })
        else:
            return Response({'error': 'Failed to score transaction'}, status=500)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


# Financial Scam Detection API

@api_view(['POST'])
def detect_scam(request):
    """
    Analyze a company for scam indicators using web scraping and data analysis.

    Request body:
    {
        "company_name": "Example Corp",
        "domain": "example.com",
        "jurisdiction": "US",
        "company_identifier": "0001234567",  // CIK or ticker (optional)
        "business_description": "...",
        "promised_returns": 15.5,
        "payment_methods": ["cryptocurrency", "wire_transfer"]
    }
    """
    try:
        # Validate request data
        request_serializer = ScamDetectionRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response({
                'error': 'Invalid request data',
                'details': request_serializer.errors
            }, status=400)

        # Extract validated data
        company_data = request_serializer.validated_data

        # Initialize scam detector
        detector = FinancialScamDetector()

        # Perform comprehensive analysis
        analysis_results = detector.analyze_company(company_data)

        # Save results to database
        scam_detection = ScamDetection.objects.create(
            company_name=company_data.get('company_name'),
            domain=company_data.get('domain'),
            company_identifier=company_data.get('company_identifier'),
            jurisdiction=company_data.get('jurisdiction', 'US'),
            overall_risk_score=analysis_results['overall_risk_score'],
            risk_level=analysis_results['risk_level'],
            category_scores=analysis_results['category_scores'],
            red_flags=analysis_results['red_flags'],
            green_flags=analysis_results['green_flags'],
            detailed_findings=analysis_results['detailed_findings'],
            recommendations=analysis_results['recommendations'],
        )

        # Serialize response
        response_serializer = ScamDetectionSerializer(scam_detection)

        return Response({
            'status': 'success',
            'message': 'Scam detection analysis completed',
            'analysis': response_serializer.data
        })

    except Exception as e:
        return Response({
            'status': 'error',
            'error': str(e),
            'message': 'Failed to complete scam detection analysis'
        }, status=500)


@api_view(['GET'])
def get_scam_detection(request, detection_id):
    """
    Retrieve a specific scam detection analysis by ID.
    """
    try:
        detection = ScamDetection.objects.get(id=detection_id)
        serializer = ScamDetectionSerializer(detection)
        return Response(serializer.data)
    except ScamDetection.DoesNotExist:
        return Response({
            'error': 'Scam detection analysis not found'
        }, status=404)


@api_view(['GET'])
def list_scam_detections(request):
    """
    List all scam detection analyses with optional filtering.

    Query parameters:
    - risk_level: Filter by risk level (low, medium, high, critical)
    - company_name: Search by company name
    - limit: Number of results to return (default 50)
    """
    try:
        queryset = ScamDetection.objects.all()

        # Apply filters
        risk_level = request.query_params.get('risk_level')
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)

        company_name = request.query_params.get('company_name')
        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)

        # Limit results
        limit = int(request.query_params.get('limit', 50))
        queryset = queryset[:limit]

        serializer = ScamDetectionListSerializer(queryset, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)


@api_view(['GET'])
def get_high_risk_companies(request):
    """
    Get all companies flagged as high or critical risk.
    """
    try:
        high_risk = ScamDetection.objects.filter(
            risk_level__in=['high', 'critical']
        ).order_by('-overall_risk_score')

        serializer = ScamDetectionListSerializer(high_risk, many=True)
        return Response({
            'count': len(serializer.data),
            'high_risk_companies': serializer.data
        })

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)