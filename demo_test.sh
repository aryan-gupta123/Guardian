#!/bin/bash

echo "🛡️  GUARDIAN FRAUD DETECTION - Demo Test"
echo "========================================"
echo ""

echo "📊 Step 1: Creating a suspicious transaction..."
RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/ingest/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000,
    "merchant": "Sketchy Electronics Store",
    "timestamp": "2025-10-25T03:00:00Z"
  }')

TXN_ID=$(echo $RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "✅ Transaction created: ID = $TXN_ID"
echo ""

echo "🤖 Step 2: Claude analyzing with Fetch.ai agent..."
curl -X POST http://127.0.0.1:8000/api/agents/act/ \
  -H "Content-Type: application/json" \
  -d "{\"transaction_id\": $TXN_ID, \"action\": \"investigate\"}" | jq '.'

echo ""
echo "📄 Step 3: View generated artifact:"
echo "http://127.0.0.1:8000/static/artifacts/${TXN_ID}_investigate.txt"
echo ""
echo "✅ Demo complete!"
