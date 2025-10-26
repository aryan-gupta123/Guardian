import { CheckCircle, Lock, Zap, Users, Bell, Sun, Moon } from 'lucide-react';
import { motion } from 'framer-motion';
import { GuardianLogo } from './GuardianLogo';
import { HeroAnimation } from './HeroAnimation';

export function LandingPage({ onGetStarted }) {
  const theme = 'dark';
  const toggleTheme = () => {};

  return (
    <div className="min-h-screen bg-[#0a1628]">

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid md:grid-cols-2 gap-12 items-center max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl md:text-6xl mb-6 text-white">
              Your AI Financial Safety Agent
            </h1>
            <p className="text-xl text-gray-400 mb-8 leading-relaxed">
              Automatically analyze your transactions, flag risky merchants, and protect your wallet.
            </p>
            <a 
              href="/signup/" 
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg text-lg inline-block"
            >
              Get Started
            </a>
          </motion.div>

          {/* Risk Status Card */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-blue-950/30 border border-blue-900/50 rounded-2xl p-8 backdrop-blur-sm"
          >
            <div className="space-y-6">
              <div className="flex items-center justify-between p-4 bg-blue-950/40 rounded-lg border border-blue-900/30">
                <span className="text-xl text-gray-300">Normal</span>
                <CheckCircle className="w-6 h-6 text-green-500" />
              </div>
              <div className="flex items-center justify-between p-4 bg-red-950/20 rounded-lg border border-red-900/30">
                <span className="text-xl text-gray-300">High Risk</span>
                <div className="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center">
                  <div className="w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-b-[10px] border-b-red-500"></div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Trust Badges */}
      <section className="container mx-auto px-4 py-12">
        <div className="flex justify-center items-center gap-8 flex-wrap text-gray-400">
          <div className="flex items-center gap-2">
            <Lock className="w-5 h-5" />
            <span>Bank-Level Security</span>
          </div>
          <div className="flex items-center gap-2">
            <GuardianLogo className="w-5 h-5" />
            <span>SOC 2 Certified</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle className="w-5 h-5" />
            <span>GDPR Compliant</span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl mb-4 text-white">How Guardian Protects You</h2>
          <p className="text-xl text-gray-400">
            Advanced AI technology that works 24/7 to keep your finances safe
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <div className="p-6 border border-blue-900/50 bg-blue-950/30 hover:bg-blue-950/40 transition-all backdrop-blur-sm rounded-lg">
              <div className="w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-blue-400" />
              </div>
              <h3 className="text-xl mb-3 text-white">Real-Time Detection</h3>
              <p className="text-gray-400 leading-relaxed">
                Our AI analyzes every transaction instantly, detecting fraud and scams 
                before they can harm you. Get alerts within seconds.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="p-6 border border-blue-900/50 bg-blue-950/30 hover:bg-blue-950/40 transition-all backdrop-blur-sm rounded-lg">
              <div className="w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center mb-4">
                <GuardianLogo className="w-6 h-6 text-blue-400" />
              </div>
              <h3 className="text-xl mb-3 text-white">Automatic Protection</h3>
              <p className="text-gray-400 leading-relaxed">
                One-click protection triggers automated workflows: dispute generation, 
                merchant unsubscribe, and card freezing—all handled for you.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="p-6 border border-blue-900/50 bg-blue-950/30 hover:bg-blue-950/40 transition-all backdrop-blur-sm rounded-lg">
              <div className="w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center mb-4">
                <Users className="w-6 h-6 text-blue-400" />
              </div>
              <h3 className="text-xl mb-3 text-white">Family Protection</h3>
              <p className="text-gray-400 leading-relaxed">
                Especially designed for seniors and vulnerable users. Voice alerts, 
                trusted contact notifications, and easy-to-understand explanations.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Interactive Animation - See Guardian in Action */}
      <section className="bg-[#050d18] border-y border-blue-950/50 relative">
        <div className="container mx-auto px-4 py-12">
          <div className="text-center bg-gradient-to-br from-blue-950/40 to-purple-950/40 border border-blue-900/30 rounded-[50px] p-8 mb-12 backdrop-blur-sm">
            <h2 className="text-4xl mb-4 text-white font-normal not-italic">See Guardian in Action</h2>
            <p className="text-xl text-gray-400 no-underline">
              Watch how Guardian detects and stops fraud before it happens
            </p>
          </div>
          <HeroAnimation />
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-[#081220] py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl mb-4 text-white">Simple, Transparent Protection</h2>
            <p className="text-xl text-gray-400">
              Guardian works seamlessly in the background—no complicated setup
            </p>
          </div>

          <div className="max-w-4xl mx-auto space-y-8">
            <div className="flex gap-6 items-start">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0">
                1
              </div>
              <div>
                <h3 className="text-xl mb-2 text-white">Connect Your Accounts</h3>
                <p className="text-gray-400">
                  Securely link your bank accounts and credit cards. We use bank-level encryption 
                  and never store your credentials.
                </p>
              </div>
            </div>

            <div className="flex gap-6 items-start">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0">
                2
              </div>
              <div>
                <h3 className="text-xl mb-2 text-white">AI Monitors 24/7</h3>
                <p className="text-gray-400">
                  Guardian's AI analyzes every transaction using merchant intelligence, anomaly 
                  detection, and pattern recognition to spot suspicious activity instantly.
                </p>
              </div>
            </div>

            <div className="flex gap-6 items-start">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0">
                3
              </div>
              <div>
                <h3 className="text-xl mb-2 text-white">Take Action in One Click</h3>
                <p className="text-gray-400">
                  When something suspicious is detected, Guardian alerts you with clear explanations. 
                  Protect yourself with one tap—we handle the rest.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl mb-4 text-white">Honest, Transparent Pricing</h2>
          <p className="text-xl text-gray-400">
            No hidden fees. Cancel anytime. Your security is our priority.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="p-8 border border-blue-900/50 bg-blue-950/20 backdrop-blur-sm rounded-lg">
            <div className="mb-6">
              <h3 className="text-2xl mb-2 text-white">Starter</h3>
              <div className="mb-4">
                <span className="text-4xl text-white">$9</span>
                <span className="text-gray-400">/month</span>
              </div>
              <p className="text-gray-400">Perfect for individuals</p>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Up to 3 accounts
              </li>
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Real-time alerts
              </li>
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Basic protection
              </li>
            </ul>
            <button className="w-full border border-blue-700 text-blue-400 hover:bg-blue-950/50 px-4 py-2 rounded">
              Start Free Trial
            </button>
          </div>

          <div className="p-8 border border-blue-500 bg-blue-950/40 backdrop-blur-sm relative rounded-lg">
            <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-3 py-1 rounded-full text-sm">
              Most Popular
            </span>
            <div className="mb-6">
              <h3 className="text-2xl mb-2 text-white">Family</h3>
              <div className="mb-4">
                <span className="text-4xl text-white">$19</span>
                <span className="text-gray-400">/month</span>
              </div>
              <p className="text-gray-400">Best for families</p>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Up to 10 accounts
              </li>
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Trusted contacts
              </li>
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Voice alerts
              </li>
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Priority support
              </li>
            </ul>
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
              Start Free Trial
            </button>
          </div>

          <div className="p-8 border border-blue-900/50 bg-blue-950/20 backdrop-blur-sm rounded-lg">
            <div className="mb-6">
              <h3 className="text-2xl mb-2 text-white">Enterprise</h3>
              <div className="mb-4">
                <span className="text-4xl text-white">Custom</span>
              </div>
              <p className="text-gray-400">For organizations</p>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Unlimited accounts
              </li>
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Advanced analytics
              </li>
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Custom integrations
              </li>
              <li className="flex items-center gap-2 text-gray-300">
                <CheckCircle className="w-5 h-5 text-green-500" />
                Dedicated support
              </li>
            </ul>
            <button className="w-full border border-blue-700 text-blue-400 hover:bg-blue-950/50 px-4 py-2 rounded">
              Contact Sales
            </button>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl mb-4">Ready to Protect Your Finances?</h2>
          <p className="text-xl mb-8 text-blue-100 max-w-2xl mx-auto">
            Join thousands of families who trust Guardian to keep their money safe. 
            Start your free 14-day trial today—no credit card required.
          </p>
          <a 
            href="/signup/"
            className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 rounded-lg text-lg inline-block"
          >
            Get Started Free
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#050d18] text-gray-400 py-12 border-t border-blue-950/50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <GuardianLogo className="w-6 h-6 text-blue-500" />
                <span className="text-white">Guardian</span>
              </div>
              <p className="text-sm">
                AI-powered financial safety for everyone.
              </p>
            </div>
            <div>
              <h4 className="text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li>Features</li>
                <li>Pricing</li>
                <li>Security</li>
                <li>Demo</li>
              </ul>
            </div>
            <div>
              <h4 className="text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li>About</li>
                <li>Blog</li>
                <li>Careers</li>
                <li>Contact</li>
              </ul>
            </div>
            <div>
              <h4 className="text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li>Privacy Policy</li>
                <li>Terms of Service</li>
                <li>Security</li>
                <li>Compliance</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-sm text-center">
            © 2024 Guardian. All rights reserved. Your security is our mission.
          </div>
        </div>
      </footer>
    </div>
  );
}