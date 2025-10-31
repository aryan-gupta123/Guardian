from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from types import SimpleNamespace
from .models import Transaction, Merchant
from .serializers import TransactionSerializer, MerchantSerializer
from .services.ml.anomaly_detector import AnomalyDetector
from .services.ml.explainability import ExplainabilityService
from .services.agents.orchestrator import ActOrchestrator
from .services.data.brightdata import merchant_intel  # optional Bright Data

# --------------------
# Homepage
# --------------------
def homepage(request):
    return render(request, 'homepage.html')


# --------------------
# API: Ingest
# --------------------
@api_view(['POST'])
def ingest_transaction(request):
    """
    Ingests a new transaction for analysis.
    - auto-creates demo user if user_id missing
    - accepts merchant as string or ID
    """
    try:
        data = request.data.copy()

        # 1️⃣ Ensure user_id
        if not data.get('user_id'):
            User = get_user_model()
            demo_user, _ = User.objects.get_or_create(username='demo')
            data['user_id'] = demo_user.id

        # 2️⃣ Normalize merchant (accepts name or ID)
        merchant_val = data.get('merchant')
        if merchant_val is None:
            return Response({"merchant": ["This field is required."]}, status=400)
        if isinstance(merchant_val, str):
            if merchant_val.isdigit():
                data['merchant'] = int(merchant_val)
            else:
                m, _ = Merchant.objects.get_or_create(name=merchant_val.strip())
                data['merchant'] = m.id

        # 3️⃣ Validate timestamp
        if 'timestamp' in data and data['timestamp']:
            dt = parse_datetime(str(data['timestamp']))
            if dt is None:
                return Response({"timestamp": ["Invalid datetime format. Use ISO 8601."]}, status=400)

        # 4️⃣ Save + score
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()

        detector = AnomalyDetector()
        risk_score, is_anomaly = detector.score_transaction(transaction)
        transaction.risk_score = risk_score
        transaction.is_anomaly = is_anomaly
        transaction.save()

        return Response({
            "id": transaction.id,
            "risk_score": risk_score,
            "is_anomaly": is_anomaly,
            "status": "success"
        }, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# --------------------
# API: Score
# --------------------
@api_view(['GET'])
def score_transaction(request, transaction_id):
    """Get risk score for a specific transaction"""
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        return Response({
            "transaction_id": transaction.id,
            "risk_score": transaction.risk_score,
            "is_anomaly": transaction.is_anomaly,
            "amount": transaction.amount,
            "merchant": transaction.merchant.name if transaction.merchant else None
        })
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=404)


# --------------------
# API: Explain
# --------------------
@api_view(['GET'])
def explain_transaction(request, transaction_id):
    """Get explanation for a transaction's risk score"""
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        explainer = ExplainabilityService()
        explanation = explainer.explain_transaction(transaction)
        return Response(explanation)
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=404)


# --------------------
# API: Agent Action (protect / dispute)
# --------------------
@api_view(['POST'])
def agent_action(request):
    """
    Trigger the Guardian agent action.
    Uses the Orchestrator to generate an artifact and rationale.
    Accepts numeric or free-form transaction_id.
    """
    try:
        action = request.data.get("action", "dispute_draft")
        ref = request.data.get("transaction_id") or request.data.get("txn_id")

        if not ref:
            return Response({"error": "Missing transaction_id"}, status=400)

        # Try to get the transaction (if numeric)
        txn_id_str = str(ref)
        try:
            txn_pk = int(ref)
            txn = Transaction.objects.get(pk=txn_pk)
            txn_id_str = str(txn.id)
        except (ValueError, Transaction.DoesNotExist):
            txn = None  # allow free-form ref

        # Run orchestrator
        result = ActOrchestrator().run(action=action, txn_id=txn_id_str)

        # Optionally update DB status if txn exists
        if txn:
            if action == "block":
                txn.status = "blocked"
            elif action == "allow":
                txn.status = "allowed"
            elif action == "investigate":
                txn.status = "under_investigation"
            txn.save()

        return Response(result, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# --------------------
# API: Merchant Info
# --------------------
@api_view(['GET'])
def get_merchant(request, merchant_id):
    """Get merchant info + optional Bright Data enrichment"""
    try:
        merchant = Merchant.objects.get(id=merchant_id)
        serializer = MerchantSerializer(merchant)
        data = serializer.data

        # optional enrichment
        try:
            enrichment = merchant_intel(merchant.name)
            data.update(enrichment)
        except Exception:
            pass

        return Response(data)
    except Merchant.DoesNotExist:
        return Response({"error": "Merchant not found"}, status=404)


# --------------------
# API: High-Risk List
# --------------------
@api_view(['GET'])
def get_high_risk_transactions(request):
    """List all high-risk transactions"""
    try:
        high_risk_transactions = Transaction.objects.filter(
            is_anomaly=True,
            status__in=["pending", "under_investigation"]
        ).order_by("-created_at")
        serializer = TransactionSerializer(high_risk_transactions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


# --------------------
# API: ML Score
# --------------------
@api_view(['POST'])
def ml_score_transaction(request):
    """
    Score a transaction using ML without saving it to database.
    Useful for real-time scoring of transactions.
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['amount', 'merchant']
        for field in required_fields:
            if field not in data:
                return Response({f"{field}": ["This field is required."]}, status=400)
        
        # Resolve merchant details
        merchant_value = data.get('merchant')
        merchant_name = data.get('merchant_name') or data.get('merchant_display') or None
        merchant_obj = None
        
        if isinstance(merchant_value, int):
            merchant_obj = Merchant.objects.filter(id=merchant_value).first()
            if not merchant_obj and merchant_name:
                merchant_obj = SimpleNamespace(name=str(merchant_name))
            elif not merchant_obj:
                merchant_obj = SimpleNamespace(name=f"Merchant {merchant_value}")
        elif merchant_value:
            merchant_obj = SimpleNamespace(name=str(merchant_value))
        
        # Construct timestamp for scoring
        timestamp = None
        if data.get('timestamp'):
            timestamp = parse_datetime(str(data.get('timestamp')))
        elif data.get('hour') is not None:
            now = timezone.now()
            try:
                hour = int(data.get('hour'))
                timestamp = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            except (ValueError, TypeError):
                timestamp = now
        else:
            timestamp = timezone.now()
        
        transaction = SimpleNamespace(
            amount=data.get('amount', 0),
            merchant=merchant_obj,
            timestamp=timestamp,
            risk_score=data.get('risk_score', 0),
            features=data.get('features', {})
        )
        
        # Score using ML
        detector = AnomalyDetector()
        risk_score, is_anomaly = detector.score_transaction(transaction)
        
        return Response({
            "risk_score": risk_score,
            "is_anomaly": is_anomaly,
            "status": "success"
        }, status=200)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)
