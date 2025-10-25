import React, { useState, useEffect } from 'react'
import { TrendingUp, AlertTriangle, Shield, Activity } from 'lucide-react'
import axios from 'axios'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalTransactions: 0,
    anomaliesDetected: 0,
    riskScore: 0,
    activeAlerts: 0
  })
  
  const [recentTransactions, setRecentTransactions] = useState([])
  
  useEffect(() => {
    // Fetch dashboard data
    fetchDashboardData()
  }, [])
  
  const fetchDashboardData = async () => {
    try {
      // This would normally fetch from your Django API
      // For now, we'll use mock data
      setStats({
        totalTransactions: 1247,
        anomaliesDetected: 23,
        riskScore: 0.15,
        activeAlerts: 5
      })
      
      setRecentTransactions([
        {
          id: 1,
          merchant: 'Amazon',
          amount: 299.99,
          riskScore: 0.85,
          isAnomaly: true,
          timestamp: new Date().toISOString()
        },
        {
          id: 2,
          merchant: 'Local Coffee Shop',
          amount: 4.50,
          riskScore: 0.12,
          isAnomaly: false,
          timestamp: new Date().toISOString()
        }
      ])
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }
  
  const statCards = [
    {
      title: 'Total Transactions',
      value: stats.totalTransactions.toLocaleString(),
      icon: Activity,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10'
    },
    {
      title: 'Anomalies Detected',
      value: stats.anomaliesDetected,
      icon: AlertTriangle,
      color: 'text-red-400',
      bgColor: 'bg-red-500/10'
    },
    {
      title: 'Avg Risk Score',
      value: (stats.riskScore * 100).toFixed(1) + '%',
      icon: TrendingUp,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10'
    },
    {
      title: 'Active Alerts',
      value: stats.activeAlerts,
      icon: Shield,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10'
    }
  ]
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-400">System Active</span>
        </div>
      </div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div key={index} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 mb-1">{stat.title}</p>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
              </div>
              <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Recent Transactions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold text-white mb-4">Recent High-Risk Transactions</h2>
          <div className="space-y-3">
            {recentTransactions.filter(t => t.isAnomaly).map(transaction => (
              <div key={transaction.id} className="flex items-center justify-between p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                <div>
                  <p className="font-medium text-white">{transaction.merchant}</p>
                  <p className="text-sm text-gray-400">${transaction.amount}</p>
                </div>
                <div className="text-right">
                  <p className="text-red-400 font-medium">{(transaction.riskScore * 100).toFixed(1)}%</p>
                  <p className="text-xs text-gray-400">High Risk</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold text-white mb-4">System Status</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-300">ML Model Status</span>
              <span className="text-green-400 font-medium">Active</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-300">Database Connection</span>
              <span className="text-green-400 font-medium">Connected</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-300">API Endpoints</span>
              <span className="text-green-400 font-medium">Healthy</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-300">Guardian Mode</span>
              <span className="text-blue-400 font-medium">Enabled</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

