import React, { useState, useEffect } from 'react'
import { Search, Filter, AlertTriangle, CheckCircle } from 'lucide-react'

const RiskTable = () => {
  const [transactions, setTransactions] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [filterRisk, setFilterRisk] = useState('all')
  
  useEffect(() => {
    // Mock data - replace with actual API call
    setTransactions([
      {
        id: 1,
        merchant: 'Amazon',
        amount: 299.99,
        riskScore: 0.85,
        isAnomaly: true,
        timestamp: '2024-01-15T10:30:00Z',
        user_id: 'user_123',
        status: 'flagged'
      },
      {
        id: 2,
        merchant: 'Local Coffee Shop',
        amount: 4.50,
        riskScore: 0.12,
        isAnomaly: false,
        timestamp: '2024-01-15T09:15:00Z',
        user_id: 'user_456',
        status: 'approved'
      },
      {
        id: 3,
        merchant: 'Gas Station',
        amount: 45.00,
        riskScore: 0.23,
        isAnomaly: false,
        timestamp: '2024-01-15T08:45:00Z',
        user_id: 'user_789',
        status: 'approved'
      },
      {
        id: 4,
        merchant: 'Unknown Merchant',
        amount: 1500.00,
        riskScore: 0.92,
        isAnomaly: true,
        timestamp: '2024-01-15T07:20:00Z',
        user_id: 'user_101',
        status: 'blocked'
      }
    ])
  }, [])
  
  const filteredTransactions = transactions.filter(transaction => {
    const matchesSearch = transaction.merchant.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         transaction.user_id.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesFilter = filterRisk === 'all' ||
                         (filterRisk === 'high' && transaction.riskScore > 0.7) ||
                         (filterRisk === 'medium' && transaction.riskScore > 0.3 && transaction.riskScore <= 0.7) ||
                         (filterRisk === 'low' && transaction.riskScore <= 0.3)
    
    return matchesSearch && matchesFilter
  })
  
  const getRiskColor = (score) => {
    if (score > 0.7) return 'text-red-400'
    if (score > 0.3) return 'text-yellow-400'
    return 'text-green-400'
  }
  
  const getStatusIcon = (status) => {
    switch (status) {
      case 'flagged':
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />
      case 'blocked':
        return <AlertTriangle className="h-4 w-4 text-red-400" />
      case 'approved':
        return <CheckCircle className="h-4 w-4 text-green-400" />
      default:
        return null
    }
  }
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Risk Assessment Table</h1>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search transactions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10 w-64"
            />
          </div>
          <select
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
            className="input-field"
          >
            <option value="all">All Risk Levels</option>
            <option value="high">High Risk</option>
            <option value="medium">Medium Risk</option>
            <option value="low">Low Risk</option>
          </select>
        </div>
      </div>
      
      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-dark-700">
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Transaction ID</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Merchant</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Amount</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Risk Score</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Status</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Timestamp</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTransactions.map(transaction => (
                <tr key={transaction.id} className="border-b border-dark-700 hover:bg-dark-700/50">
                  <td className="py-3 px-4 text-white font-mono text-sm">#{transaction.id}</td>
                  <td className="py-3 px-4 text-white">{transaction.merchant}</td>
                  <td className="py-3 px-4 text-white font-medium">${transaction.amount}</td>
                  <td className="py-3 px-4">
                    <span className={`font-medium ${getRiskColor(transaction.riskScore)}`}>
                      {(transaction.riskScore * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(transaction.status)}
                      <span className="capitalize text-gray-300">{transaction.status}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-gray-400 text-sm">
                    {new Date(transaction.timestamp).toLocaleString()}
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex space-x-2">
                      <button className="btn-primary text-xs px-3 py-1">
                        Review
                      </button>
                      <button className="btn-secondary text-xs px-3 py-1">
                        Explain
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default RiskTable

