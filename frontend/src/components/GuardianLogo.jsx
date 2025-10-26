import React from 'react';

export function GuardianLogo({ className = "w-8 h-8" }) {
  return (
    <svg 
      className={className} 
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Shield shape */}
      <path 
        d="M50 5 L85 25 L85 60 L50 95 L15 60 L15 25 Z" 
        fill="currentColor" 
        fillOpacity="0.1"
        stroke="currentColor"
        strokeWidth="2"
      />
      
      {/* Inner shield design */}
      <path 
        d="M50 15 L75 30 L75 55 L50 80 L25 55 L25 30 Z" 
        fill="currentColor" 
        fillOpacity="0.2"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      
      {/* Center symbol - stylized "G" */}
      <path 
        d="M50 35 C45 35, 40 40, 40 50 C40 60, 45 65, 50 65 C55 65, 60 60, 60 50 L55 50 C55 55, 52.5 57.5, 50 57.5 C47.5 57.5, 45 55, 45 50 C45 45, 47.5 42.5, 50 42.5 C52.5 42.5, 55 45, 55 50 L60 50 C60 40, 55 35, 50 35 Z" 
        fill="currentColor"
        fillOpacity="0.8"
      />
      
      {/* Protective border */}
      <circle 
        cx="50" 
        cy="50" 
        r="42" 
        fill="none" 
        stroke="currentColor" 
        strokeWidth="1" 
        strokeOpacity="0.3"
      />
    </svg>
  );
}
