import React, { useState } from 'react'

export default function LandingPage({ initial = {}, onCreate }){
  const [location, setLocation] = useState(initial.location || '')
  const [month, setMonth] = useState(initial.month || '')
  const [budget, setBudget] = useState(initial.budget || '')
  const [activityType, setActivityType] = useState(initial.activityType || '')

  const handleSubmit = (e) => {
    e && e.preventDefault()
    const payload = { location, month, budget, activityType }
    onCreate && onCreate(payload)
  }

  return (
    <div className="relative flex items-center justify-center min-h-screen px-4 bg-gradient-to-b from-yellow-100 via-amber-50 to-sky-50 overflow-hidden">
      {/* Decorative SVGs — sun (top-left), waves (bottom), island+palm (bottom-right) */}
      <div className="pointer-events-none">
        <svg className="absolute -top-32 -left-32 w-96 h-96" viewBox="0 0 140 140" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
          <defs>
            <linearGradient id="gSunBig" x1="0" x2="1">
              <stop offset="0%" stopColor="#FFD166" />
              <stop offset="100%" stopColor="#FF9A76" />
            </linearGradient>
          </defs>
          {/* longer rays (drawn first so the circle sits on top) */}
          <g stroke="#FFB366" strokeWidth="4" strokeLinecap="round">
            {/* 8 evenly spaced rays; start at radius 54, end at radius 72 from center (60,60) */}
            <line x1="114.0" y1="60.0" x2="132.0" y2="60.0" />
            <line x1="98.2" y1="98.2" x2="110.9" y2="110.9" />
            <line x1="60.0" y1="114.0" x2="60.0" y2="132.0" />
            <line x1="21.8" y1="98.2" x2="9.1" y2="110.9" />
            <line x1="6.0" y1="60.0" x2="-12.0" y2="60.0" />
            <line x1="21.8" y1="21.8" x2="9.1" y2="9.1" />
            <line x1="60.0" y1="6.0" x2="60.0" y2="-12.0" />
            <line x1="98.2" y1="21.8" x2="110.9" y2="9.1" />
          </g>
          {/* large sun circle — placed so part of it sits off-canvas top-left */}
          <circle cx="60" cy="60" r="48" fill="url(#gSunBig)" />
        </svg>

        <svg className="absolute bottom-0 left-0 w-full h-40" viewBox="0 0 1440 320" preserveAspectRatio="none" aria-hidden>
          <path fill="#7AD7F0" fillOpacity="1" d="M0,224L48,213.3C96,203,192,181,288,160C384,139,480,117,576,106.7C672,96,768,96,864,101.3C960,107,1056,117,1152,122.7C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>

      </div>

      <div className="w-full max-w-2xl">
        <div className="relative text-center">
          <h1 className="text-7xl font-extrabold mb-4 py-4 text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-pink-500">Perfect Day</h1>
          <form onSubmit={handleSubmit} className="space-y-4 text-left">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

              <label className="block">
                <span className="text-sm font-medium text-slate-700">Location</span>
                <input value={location} onChange={e=>setLocation(e.target.value)} className="mt-1 block w-full p-3 border border-transparent rounded-lg shadow-sm" placeholder="e.g. Bora Bora" />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-slate-700">Month</span>
                <input value={month} onChange={e=>setMonth(e.target.value)} className="mt-1 block w-full p-3 border border-transparent rounded-lg shadow-sm" placeholder="e.g. December" />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-slate-700">Budget</span>
                <input value={budget} onChange={e=>setBudget(e.target.value)} className="mt-1 block w-full p-3 border border-transparent rounded-lg shadow-sm" placeholder="e.g. 2000" />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-slate-700">Activity type</span>
                <input value={activityType} onChange={e=>setActivityType(e.target.value)} className="mt-1 block w-full p-3 border border-transparent rounded-lg shadow-sm" placeholder="e.g. snorkeling, hiking" />
              </label>

            </div>

            <div className="text-center pt-4">
              <button type="submit" className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-full shadow">Create Itinerary</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
