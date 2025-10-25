import React, { useState, useEffect } from 'react'
import { Bot, Shield, AlertTriangle, CheckCircle, XCircle, Search } from 'lucide-react'

const AgentActions = () => {
  const [actions, setActions] = useState([])
  const [selectedAction, setSelectedAction] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  
  useEffect(() => {
    // Mock data - replace with actual API call
    setActions([
      {
        id: 1,
        transaction_id: 1,
        action_type: 'block',
        reason: 'High risk score detected with unusual spending pattern',
        confidence: 0.92,
        timestamp: '2024-01-15T10:35:00Z',
        status: 'completed',
        transaction: {
          merchant: 'Amazon',
          amount: 299.99,
          riskScore: 0.85
        }
      },
      {
        id: 2,
        transaction_id: 2,
        action_type: 'flag',
        reason: 'Merchant not in user\'s typical spending categories',
        confidence: 0.78,
        timestamp: '2024-01-15T09:20:00Z',
        status: 'pending',
        transaction: {
          merchant: 'Unknown Merchant',
          amount: 1500.00,
          riskScore: 0.92
        }
      },
      {
        id: 3,
        transaction_id: 3,
        action_type: 'approve',
        reason: 'Low risk transaction within normal parameters',
        confidence: 0.95,
        timestamp: '2024-01-15T08:50:00Z',
        status: 'completed',
        transaction: {
          merchant: 'Local Coffee Shop',
          amount: 4.50,
          riskScore: 0.12
        }
      }
    ])
  }, [])
  
  const filteredActions = actions.filter(action =>
    action.transaction.merchant.toLowerCase().includes(searchTerm.toLowerCase()) ||
    action.action_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    action.reason.toLowerCase().includes(searchTerm.toLowerCase())
  )
  
  const getActionIcon = (actionType) => {
    switch (actionType) {
      case 'block':
        return <XCircle className="h-5 w-5 text-red-400" />
      case 'flag':
        return <AlertTriangle className="h-5 w-5 text-yellow-400" />
      case 'approve':
        return <CheckCircle className="h-5 w-5 text-green-400" />
      case 'investigate':
        return <Search className="h-5 w-5 text-blue-400" />
      default:
        return <Bot className="h-5 w-5 text-gray-400" />
    }
  }
  
  const getActionColor = (actionType) => {
    switch (actionType) {
      case 'block':
        return 'bg-red-500/10 border-red-500/20 text-red-400'
      case 'flag':
        return 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400'
      case 'approve':
        return 'bg-green-500/10 border-green-500/20 text-green-400'
      case 'investigate':
        return 'bg-blue-500/10 border-blue-500/20 text-blue-400'
      default:
        return 'bg-gray-500/10 border-gray-500/20 text-gray-400'
    }
  }
  
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'text-green-400'
      case 'pending':
        return 'text-yellow-400'
      case 'failed':
        return 'text-red-400'
      default:
        return 'text-gray-400'
    }
  }
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Agent Actions</h1>
        <div className="flex items-center space-x-2">
          <Bot className="h-6 w-6 text-primary-500" />
          <span className="text-sm text-gray-400">AI Agent System</span>
        </div>
      </div>
      
      {/* Search and Filters */}
      <div className="card">
        <div className="flex items-center space-x-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search actions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10 w-full"
            />
          </div>
          <div className="flex space-x-2">
            <button className="btn-primary">All Actions</button>
            <button className="btn-secondary">Pending</button>
            <button className="btn-secondary">Completed</button>
          </div>
        </div>
      </div>
      
      {/* Actions List */}
      <div className="space-y-4">
        {filteredActions.map(action => (
          <div key={action.id} className="card">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  {getActionIcon(action.action_type)}
                  <div>
                    <h3 className="font-semibold text-white capitalize">
                      {action.action_type} Transaction
                    </h3>
                    <p className="text-sm text-gray-400">
                      Transaction #{action.transaction_id} - {action.transaction.merchant}
                    </p>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-gray-400 mb-1">Transaction Details</p>
                    <p className="text-white font-medium">${action.transaction.amount}</p>
                    <p className="text-sm text-gray-400">
                      Risk: {(action.transaction.riskScore * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400 mb-1">Confidence</p>
                    <p className="text-white font-medium">
                      {(action.confidence * 100).toFixed(1)}%
                    </p>
                    <div className="w-full bg-dark-700 rounded-full h-2 mt-1">
                      <div 
                        className="bg-primary-500 h-2 rounded-full" 
                        style={{ width: `${action.confidence * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400 mb-1">Status</p>
                    <p className={`font-medium ${getStatusColor(action.status)}`}>
                      {action.status.charAt(0).toUpperCase() + action.status.slice(1)}
                    </p>
                  </div>
                </div>
                
                <div className="bg-dark-700 rounded-lg p-3">
                  <p className="text-sm text-gray-400 mb-1">Agent Reasoning</p>
                  <p className="text-white">{action.reason}</p>
                </div>
              </div>
              
              <div className="ml-4 flex flex-col space-y-2">
                <button 
                  className={`px-3 py-1 rounded-lg text-sm font-medium border ${getActionColor(action.action_type)}`}
                >
                  {action.action_type.charAt(0).toUpperCase() + action.action_type.slice(1)}
                </button>
                <button className="btn-secondary text-xs px-3 py-1">
                  View Details
                </button>
                {action.status === 'pending' && (
                  <button className="btn-primary text-xs px-3 py-1">
                    Review
                  </button>
                )}
              </div>
            </div>
            
            <div className="mt-4 pt-4 border-t border-dark-700">
              <div className="flex items-center justify-between text-sm text-gray-400">
                <span>Action ID: #{action.id}</span>
                <span>{new Date(action.timestamp).toLocaleString()}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {filteredActions.length === 0 && (
        <div className="card">
          <div className="text-center py-12">
            <Bot className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-400">No agent actions found</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default AgentActions

