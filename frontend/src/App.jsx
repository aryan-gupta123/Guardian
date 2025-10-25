import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import RiskTable from './components/RiskTable'
import ExplainPanel from './components/ExplainPanel'
import AgentActions from './components/AgentActions'
import Navbar from './components/Navbar'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-dark-900">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/risk-table" element={<RiskTable />} />
            <Route path="/explain" element={<ExplainPanel />} />
            <Route path="/agents" element={<AgentActions />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

