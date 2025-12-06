import React from 'react'
import MotorControl from './MotorControl'
import ServoControl from './ServoControl'
import DiseaseDetection from './DiseaseDetection'

function Dashboard() {
  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Header */}
      <header className="mb-8 text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
          🍅 Agri ROBO
        </h1>
        <p className="text-white/90 text-lg">
          Tomato Disease Detection & Robot Control System
        </p>
      </header>

      {/* Dashboard Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Motor Control Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 transform transition-all hover:scale-105">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span className="text-3xl">🤖</span>
            Robot Motor Control
          </h2>
          <MotorControl />
        </div>

        {/* Servo Control Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 transform transition-all hover:scale-105">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span className="text-3xl">💧</span>
            Fertilizer Dispenser
          </h2>
          <ServoControl />
        </div>

        {/* Disease Detection Card - Full Width */}
        <div className="lg:col-span-2 bg-white rounded-2xl shadow-2xl p-6 transform transition-all hover:scale-[1.01]">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span className="text-3xl">🔍</span>
            Leaf Disease Detection
          </h2>
          <DiseaseDetection />
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-8 text-center text-white/80 text-sm">
        <p>Agri ROBO System - Powered by AI & IoT</p>
      </footer>
    </div>
  )
}

export default Dashboard

