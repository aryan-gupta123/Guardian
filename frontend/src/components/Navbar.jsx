import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Shield, BarChart3, Brain, Settings, Sun, Moon } from 'lucide-react'
import { GuardianLogo } from './GuardianLogo'

const Navbar = () => {
  const location = useLocation()
  const theme = 'dark'
  const toggleTheme = () => {}
  
  return (
    <nav className="border-b border-blue-950/50 bg-[#0a1628]/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <GuardianLogo className="w-8 h-8 text-white" />
            <span className="text-2xl text-white">Guardian</span>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-gray-300 hover:text-white hover:bg-blue-950/50 px-3 py-2 rounded">Features</button>
            <button className="text-gray-300 hover:text-white hover:bg-blue-950/50 px-3 py-2 rounded">Pricing</button>
            <button className="text-gray-300 hover:text-white hover:bg-blue-950/50 px-3 py-2 rounded">About</button>
            <button 
              onClick={toggleTheme}
              className="text-gray-300 hover:text-white hover:bg-blue-950/50 p-2 rounded"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            <a href="/login/" className="text-gray-300 hover:text-white hover:bg-transparent px-3 py-2 rounded">Login</a>
            <a href="/signup/" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
              Sign Up
            </a>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

