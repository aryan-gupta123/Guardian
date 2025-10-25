import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import RiskTable from './components/RiskTable'
import ExplainPanel from './components/ExplainPanel'
import AgentActions from './components/AgentActions'
import Navbar from './components/Navbar'
import { LandingPage } from './components/LandingPage'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
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

