import { useRef, useEffect, useState } from 'react';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import { GuardianLogo } from './GuardianLogo';
import { AlertTriangle, CheckCircle2, DollarSign } from 'lucide-react';

export function HeroAnimation() {
  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"]
  });

  // Smooth spring animation for scroll progress
  const smoothProgress = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  });

  // Animation stages based on scroll - COMPRESSED TIMELINE
  const riskValue = useTransform(smoothProgress, [0, 0.25, 0.4, 0.5], [12, 35, 75, 85]);
  const transactionY = useTransform(smoothProgress, [0, 0.1], [100, 0]);
  const transactionOpacity = useTransform(smoothProgress, [0, 0.1], [0, 1]);
  
  // Impending danger effects (showing threat BEFORE Guardian arrives)
  const dangerPulse = useTransform(smoothProgress, [0.45, 0.55], [0, 1]);
  const warningOpacity = useTransform(smoothProgress, [0.45, 0.5, 0.55], [0, 1, 1]);
  const cardShake = useTransform(smoothProgress, [0.45, 0.55], [0, 1]);
  const crackOpacity = useTransform(smoothProgress, [0.48, 0.55, 0.65], [0, 1, 0]);
  const redVignetteOpacity = useTransform(smoothProgress, [0.45, 0.55], [0, 0.6]);
  
  // Risk factor popups (appearing during risk climb)
  const foreignTxOpacity = useTransform(smoothProgress, [0.15, 0.2, 0.5, 0.55], [0, 1, 1, 0]);
  const timeOfDayOpacity = useTransform(smoothProgress, [0.22, 0.27, 0.5, 0.55], [0, 1, 1, 0]);
  const frequencyOpacity = useTransform(smoothProgress, [0.29, 0.34, 0.5, 0.55], [0, 1, 1, 0]);
  const amountOpacity = useTransform(smoothProgress, [0.36, 0.41, 0.5, 0.55], [0, 1, 1, 0]);
  
  // Guardian entrance
  const guardianScale = useTransform(smoothProgress, [0.55, 0.65], [0, 1]);
  const guardianY = useTransform(smoothProgress, [0.55, 0.65], [-100, 0]);
  const guardianOpacity = useTransform(smoothProgress, [0.55, 0.6], [0, 1]);
  
  // Shield glow and scanning effect
  const shieldGlow = useTransform(smoothProgress, [0.6, 0.75], [0, 1]);
  const scanLineY = useTransform(smoothProgress, [0.6, 0.7], [-50, 50]);
  
  // Background blur when Guardian appears
  const backgroundBlur = useTransform(smoothProgress, [0.55, 0.65], [0, 8]);
  const backgroundDim = useTransform(smoothProgress, [0.55, 0.65], [1, 0.3]);
  
  // Success state
  const successOpacity = useTransform(smoothProgress, [0.72, 0.82], [0, 1]);
  const successScale = useTransform(smoothProgress, [0.72, 0.82], [0.8, 1]);

  const [currentRisk, setCurrentRisk] = useState(12);

  useEffect(() => {
    const unsubscribe = riskValue.on('change', (latest) => {
      setCurrentRisk(Math.round(latest));
    });
    return unsubscribe;
  }, [riskValue]);

  // Determine risk color
  const getRiskColor = (risk) => {
    if (risk < 30) return 'text-green-400';
    if (risk < 60) return 'text-yellow-400';
    if (risk < 75) return 'text-orange-400';
    return 'text-red-400';
  };

  const getRiskBg = (risk) => {
    if (risk < 30) return 'bg-green-500/20 border-green-500/50';
    if (risk < 60) return 'bg-yellow-500/20 border-yellow-500/50';
    if (risk < 75) return 'bg-orange-500/20 border-orange-500/50';
    return 'bg-red-500/20 border-red-500/50';
  };

  // Particle positions (8 directions)
  const particleAngles = [0, 45, 90, 135, 180, 225, 270, 315];

  return (
    <div ref={containerRef} className="relative h-[200vh] w-full">
      <div className="sticky top-20 h-[50vh] flex items-center justify-center overflow-hidden bg-[rgba(0,0,0,0)]">
        {/* Background gradient pulse */}
        <motion.div
          className="absolute inset-0 bg-gradient-radial from-red-500/20 via-transparent to-transparent"
          style={{
            opacity: useTransform(smoothProgress, [0.4, 0.55], [0, 0.3]),
            scale: useTransform(smoothProgress, [0.4, 0.55], [0.5, 2])
          }}
        />

        {/* Intense red vignette showing impending danger */}
        <motion.div
          className="absolute inset-0 z-5"
          style={{
            opacity: redVignetteOpacity,
            background: 'radial-gradient(ellipse at center, transparent 30%, rgba(239, 68, 68, 0.4) 100%)'
          }}
        />

        {/* Background content (transaction + explosion) - gets blurred */}
        <motion.div
          className="absolute inset-0 z-10"
          style={{
            filter: backgroundBlur.get ? `blur(${backgroundBlur.get()}px)` : 'blur(0px)',
            opacity: backgroundDim
          }}
        >
          {/* Transaction Card */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
            <motion.div
              style={{ y: transactionY, opacity: transactionOpacity }}
              className="relative"
            >
              <motion.div
                className={`p-8 rounded-2xl border-2 backdrop-blur-sm transition-all duration-300 min-w-[500px] ${getRiskBg(currentRisk)}`}
                animate={{
                  scale: currentRisk > 75 ? [1, 1.05, 1] : 1,
                  x: currentRisk > 75 ? [-2, 2, -2, 2, 0] : 0
                }}
                transition={{
                  repeat: currentRisk > 75 ? Infinity : 0,
                  duration: 0.3
                }}
                style={{
                  x: cardShake.get ? cardShake.get() * (Math.sin(Date.now() / 50) * 3) : 0
                }}
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-14 h-14 rounded-full bg-blue-500/20 flex items-center justify-center">
                    <DollarSign className="w-7 h-7 text-blue-400" />
                  </div>
                  <div>
                    <h3 className="text-white text-lg">Subscription Charge</h3>
                    <p className="text-gray-400">ShopMaster Pro</p>
                  </div>
                  <div className="ml-auto text-white text-xl">-$299.99</div>
                </div>

                {/* Risk Meter */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 text-sm">Risk Score</span>
                    <motion.span className={`text-2xl font-mono ${getRiskColor(currentRisk)}`}>
                      {currentRisk}
                    </motion.span>
                  </div>
                  
                  {/* Progress bar */}
                  <div className="relative">
                    {/* Cap label - positioned above the bar */}
                    <div className="absolute -top-5 text-xs text-white whitespace-nowrap bg-gray-900/80 px-2 py-0.5 rounded" style={{ left: 'calc(75% - 24px)' }}>
                      Cap: 75
                    </div>
                    
                    <div className="h-3 bg-gray-800 rounded-full overflow-hidden relative">
                      <motion.div
                        className="h-full transition-colors duration-300"
                        style={{
                          width: `${currentRisk}%`,
                          background: currentRisk < 30 ? '#4ade80' :
                                      currentRisk < 60 ? '#facc15' :
                                      currentRisk < 75 ? '#fb923c' : '#ef4444'
                        }}
                      />
                      {/* Cap indicator line at 75 */}
                      <div className="absolute top-0 h-full w-0.5 bg-white/50" style={{ left: '75%' }} />
                    </div>
                  </div>

                  {currentRisk > 75 && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="flex items-center gap-2 text-red-400 text-sm"
                    >
                      <AlertTriangle className="w-4 h-4" />
                      <span>Threshold exceeded! Suspicious fraud attempt detected.</span>
                    </motion.div>
                  )}
                </div>
              </motion.div>

              {/* Warning symbols appearing around card (impending danger) */}
              {particleAngles.map((angle, i) => {
                const distance = 120;
                const x = Math.cos((angle * Math.PI) / 180) * distance;
                const y = Math.sin((angle * Math.PI) / 180) * distance;

                return (
                  <motion.div
                    key={i}
                    className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                    style={{
                      opacity: warningOpacity,
                      x,
                      y
                    }}
                  >
                    <motion.div
                      animate={{
                        scale: [1, 1.2, 1],
                        rotate: [0, 10, -10, 0]
                      }}
                      transition={{
                        repeat: Infinity,
                        duration: 0.8,
                        delay: i * 0.1
                      }}
                    >
                      <AlertTriangle className="w-8 h-8 text-red-500 drop-shadow-[0_0_8px_rgba(239,68,68,0.8)]" />
                    </motion.div>
                  </motion.div>
                );
              })}

              {/* Pulsing danger border (intensifying threat) */}
              <motion.div
                className="absolute inset-0 rounded-2xl border-4 border-red-500 pointer-events-none"
                style={{
                  opacity: dangerPulse
                }}
                animate={{
                  scale: [1, 1.05, 1]
                }}
                transition={{
                  repeat: Infinity,
                  duration: 0.6
                }}
              />

              {/* Cracks appearing on card (showing it's about to break/be compromised) */}
              <motion.div
                className="absolute inset-0 rounded-2xl overflow-hidden pointer-events-none"
                style={{
                  opacity: crackOpacity
                }}
              >
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 400 300">
                  <motion.path
                    d="M 200 0 L 180 80 L 220 120 L 200 180 L 190 300"
                    stroke="#ef4444"
                    strokeWidth="2"
                    fill="none"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.5 }}
                    filter="drop-shadow(0 0 4px rgba(239, 68, 68, 0.8))"
                  />
                  <motion.path
                    d="M 100 50 L 140 100 L 120 150"
                    stroke="#ef4444"
                    strokeWidth="2"
                    fill="none"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.4, delay: 0.1 }}
                    filter="drop-shadow(0 0 4px rgba(239, 68, 68, 0.8))"
                  />
                  <motion.path
                    d="M 300 40 L 260 90 L 280 140"
                    stroke="#ef4444"
                    strokeWidth="2"
                    fill="none"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.4, delay: 0.15 }}
                    filter="drop-shadow(0 0 4px rgba(239, 68, 68, 0.8))"
                  />
                </svg>
              </motion.div>

              {/* Risk factor popups */}
              {/* Foreign Transaction - Top Right */}
              <motion.div
                className="absolute -top-20 -right-10 pointer-events-none"
                style={{
                  opacity: foreignTxOpacity,
                  y: useTransform(foreignTxOpacity, [0, 1], [-10, 0])
                }}
              >
                <div className="bg-orange-500/40 border-2 border-orange-500/80 rounded-lg px-3 py-2 backdrop-blur-sm shadow-lg">
                  <p className="text-orange-200 text-xs whitespace-nowrap">Foreign Transaction <span className="text-orange-300">+15 risk</span></p>
                </div>
              </motion.div>

              {/* Time of Day - Left Side */}
              <motion.div
                className="absolute top-10 -left-32 pointer-events-none"
                style={{
                  opacity: timeOfDayOpacity,
                  x: useTransform(timeOfDayOpacity, [0, 1], [-10, 0])
                }}
              >
                <div className="bg-orange-500/40 border-2 border-orange-500/80 rounded-lg px-3 py-2 backdrop-blur-sm shadow-lg">
                  <p className="text-orange-200 text-xs whitespace-nowrap">Unusual Time <span className="text-orange-300">+12 risk</span></p>
                </div>
              </motion.div>

              {/* Frequency - Bottom Left */}
              <motion.div
                className="absolute -bottom-20 -left-16 pointer-events-none"
                style={{
                  opacity: frequencyOpacity,
                  y: useTransform(frequencyOpacity, [0, 1], [10, 0])
                }}
              >
                <div className="bg-red-500/40 border-2 border-red-500/80 rounded-lg px-3 py-2 backdrop-blur-sm shadow-lg">
                  <p className="text-red-200 text-xs whitespace-nowrap">High Frequency <span className="text-red-300">+18 risk</span></p>
                </div>
              </motion.div>

              {/* Amount - Bottom Right */}
              <motion.div
                className="absolute -bottom-16 -right-12 pointer-events-none"
                style={{
                  opacity: amountOpacity,
                  y: useTransform(amountOpacity, [0, 1], [10, 0])
                }}
              >
                <div className="bg-red-500/40 border-2 border-red-500/80 rounded-lg px-3 py-2 backdrop-blur-sm shadow-lg">
                  <p className="text-red-200 text-xs whitespace-nowrap">Large Amount <span className="text-red-300">+25 risk</span></p>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </motion.div>

        {/* Guardian Popup Modal - appears on top with blur backdrop */}
        <motion.div
          className="absolute inset-0 z-40 flex items-center justify-center"
          style={{
            opacity: guardianOpacity,
            pointerEvents: 'none'
          }}
        >
          {/* Modal backdrop */}
          <motion.div
            className="absolute inset-0 bg-black/50 backdrop-blur-md"
            style={{
              opacity: guardianOpacity
            }}
          />

          {/* Modal content */}
          <motion.div
            className="relative z-50 bg-gradient-to-br from-blue-950/90 to-purple-950/90 border-2 border-blue-500/50 rounded-3xl p-12 backdrop-blur-xl shadow-2xl"
            style={{
              scale: guardianScale,
              y: guardianY
            }}
          >
            {/* Guardian Shield with scanning animation */}
            <div className="relative mb-8">
              <motion.div
                className="relative"
                animate={{
                  rotate: [0, -5, 5, -5, 0]
                }}
                transition={{
                  duration: 0.5,
                  repeat: Infinity,
                  repeatDelay: 2
                }}
              >
                {/* Shield glow effect */}
                <motion.div
                  className="absolute inset-0 blur-3xl"
                  style={{
                    opacity: shieldGlow
                  }}
                >
                  <GuardianLogo className="w-40 h-40 text-blue-400 mx-auto" />
                </motion.div>
                
                <GuardianLogo className="w-40 h-40 text-blue-500 relative z-10 mx-auto" />

                {/* Scanning line effect */}
                <motion.div
                  className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-blue-400 to-transparent"
                  style={{
                    y: scanLineY,
                    opacity: useTransform(smoothProgress, [0.6, 0.65, 0.7, 0.72], [0, 1, 1, 0])
                  }}
                />

                {/* Pulsing rings around shield */}
                <motion.div
                  className="absolute inset-0 border-2 border-blue-400 rounded-full"
                  animate={{
                    scale: [1, 1.3, 1.3],
                    opacity: [0.5, 0, 0]
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    repeatDelay: 0.5
                  }}
                />
              </motion.div>
            </div>

            {/* Success message */}
            <motion.div
              className="text-center"
              style={{
                opacity: successOpacity,
                scale: successScale
              }}
            >
              <CheckCircle2 className="w-20 h-20 text-green-400 mx-auto mb-6" />
              <h3 className="text-4xl text-white mb-4">Transaction Blocked</h3>
              <p className="text-xl text-gray-300 max-w-md">
                Fraud attempt detected and blocked — Guardian protected your finances before any damage occurred.
              </p>
            </motion.div>
          </motion.div>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          className="absolute bottom-2 left-1/2 -translate-x-1/2 text-gray-500 text-sm z-50"
          style={{
            opacity: useTransform(smoothProgress, [0, 0.1, 0.9, 1], [1, 0, 0, 1])
          }}
        >
          ↓ Scroll to see Guardian in action
        </motion.div>
      </div>
    </div>
  );
}