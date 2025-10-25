import React, { useState, useEffect } from 'react'
import { Brain, AlertTriangle, TrendingUp, Clock, DollarSign } from 'lucide-react'

const ExplainPanel = () => {
  const [selectedTransaction, setSelectedTransaction] = useState(null)
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(false)
  
  const mockTransactions = [
    {
      id: 1,
      merchant: 'Amazon',
      amount: 299.99,
      riskScore: 0.85,
      timestamp: '2024-01-15T10:30:00Z'
    },
    {
      id: 2,
      merchant: 'Unknown Merchant',
      amount: 1500.00,
      riskScore: 0.92,
      timestamp: '2024-01-15T07:20:00Z'
    }
  ]
  
  const mockExplanation = {
    explanation: "Transaction scored -0.234 (lower is more anomalous)",
    top_features: [
      {
        feature: 'amount',
        value: 299.99,
        importance: 0.45,
        contribution: 0.23
      },
      {
        feature: 'merchant_risk_score',
        value: 0.85,
        importance: 0.32,
        contribution: 0.18
      },
      {
        feature: 'location_risk_score',
        value: 0.67,
        importance: 0.28,
        contribution: 0.15
      },
      {
        feature: 'hour_of_day',
        value: 10,
        importance: 0.15,
        contribution: 0.08
      },
      {
        feature: 'transaction_frequency',
        value: 12.5,
        importance: 0.12,
        contribution: 0.06
      }
    ],
    risk_factors: [
      {
        feature: 'amount',
        value: 299.99,
        reason: 'Unusually high amount: $299.99'
      },
      {
        feature: 'merchant_risk_score',
        value: 0.85,
        reason: 'High merchant risk: 0.85'
      },
      {
        feature: 'location_risk_score',
        value: 0.67,
        reason: 'High location risk: 0.67'
      }
    ],
    is_anomaly: true
  }
  
  const fetchExplanation = async (transactionId) => {
    setLoading(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      setExplanation(mockExplanation)
    } catch (error) {
      console.error('Error fetching explanation:', error)
    } finally {
      setLoading(false)
    }
  }
  
  const handleTransactionSelect = (transaction) => {
    setSelectedTransaction(transaction)
    fetchExplanation(transaction.id)
  }
  
  const getFeatureIcon = (feature) => {
    switch (feature) {
      case 'amount':
        return <DollarSign className="h-4 w-4" />
      case 'hour_of_day':
        return <Clock className="h-4 w-4" />
      case 'merchant_risk_score':
      case 'location_risk_score':
        return <AlertTriangle className="h-4 w-4" />
      default:
        return <TrendingUp className="h-4 w-4" />
    }
  }
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Explainability Panel</h1>
        <div className="flex items-center space-x-2">
          <Brain className="h-6 w-6 text-primary-500" />
          <span className="text-sm text-gray-400">AI-Powered Explanations</span>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Transaction Selection */}
        <div className="card">
          <h2 className="text-xl font-semibold text-white mb-4">Select Transaction</h2>
          <div className="space-y-3">
            {mockTransactions.map(transaction => (
              <button
                key={transaction.id}
                onClick={() => handleTransactionSelect(transaction)}
                className={`w-full p-3 rounded-lg border transition-colors ${
                  selectedTransaction?.id === transaction.id
                    ? 'border-primary-500 bg-primary-500/10'
                    : 'border-dark-600 hover:border-dark-500'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="text-left">
                    <p className="font-medium text-white">{transaction.merchant}</p>
                    <p className="text-sm text-gray-400">${transaction.amount}</p>
                  </div>
                  <div className="text-right">
                    <p className={`font-medium ${
                      transaction.riskScore > 0.7 ? 'text-red-400' : 
                      transaction.riskScore > 0.3 ? 'text-yellow-400' : 'text-green-400'
                    }`}>
                      {(transaction.riskScore * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
        
        {/* Explanation Results */}
        <div className="lg:col-span-2">
          {loading ? (
            <div className="card">
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
                <span className="ml-3 text-gray-400">Analyzing transaction...</span>
              </div>
            </div>
          ) : explanation ? (
            <div className="space-y-6">
              {/* Overall Explanation */}
              <div className="card">
                <h2 className="text-xl font-semibold text-white mb-4">Risk Assessment</h2>
                <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-2">
                    <AlertTriangle className="h-5 w-5 text-red-400" />
                    <span className="font-medium text-red-400">High Risk Transaction</span>
                  </div>
                  <p className="text-gray-300">{explanation.explanation}</p>
                </div>
              </div>
              
              {/* Top Contributing Features */}
              <div className="card">
                <h2 className="text-xl font-semibold text-white mb-4">Top Contributing Features</h2>
                <div className="space-y-3">
                  {explanation.top_features.map((feature, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-dark-700 rounded-lg">
                      <div className="flex items-center space-x-3">
                        {getFeatureIcon(feature.feature)}
                        <div>
                          <p className="font-medium text-white capitalize">
                            {feature.feature.replace('_', ' ')}
                          </p>
                          <p className="text-sm text-gray-400">Value: {feature.value}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-primary-400 font-medium">
                          {(feature.importance * 100).toFixed(1)}%
                        </p>
                        <p className="text-xs text-gray-400">Importance</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Risk Factors */}
              <div className="card">
                <h2 className="text-xl font-semibold text-white mb-4">Identified Risk Factors</h2>
                <div className="space-y-3">
                  {explanation.risk_factors.map((factor, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                      <AlertTriangle className="h-5 w-5 text-red-400 mt-0.5 flex-shrink-0" />
                      <div>
                        <p className="font-medium text-red-400 capitalize">
                          {factor.feature.replace('_', ' ')}
                        </p>
                        <p className="text-sm text-gray-300">{factor.reason}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="card">
              <div className="text-center py-12">
                <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-400">Select a transaction to view its explanation</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ExplainPanel

