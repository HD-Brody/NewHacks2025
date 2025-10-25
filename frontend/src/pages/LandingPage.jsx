import React, { useState } from 'react'

export default function LandingPage({ initial = {}, onCreate }){
  const [location, setLocation] = useState(initial.location || '')
  const [month, setMonth] = useState(initial.month || '')
  const [budget, setBudget] = useState(initial.budget || '')
  // activities: array of singular activity words. activityInput holds the current typed word.
  const [activities, setActivities] = useState(
    initial.activities && Array.isArray(initial.activities)
      ? initial.activities
      : (initial.activityType ? initial.activityType.split(',').map(s=>s.trim()).filter(Boolean) : [])
  )
  const [activityInput, setActivityInput] = useState('')

  const handleSubmit = (e) => {
    e && e.preventDefault()
    // keep backward compatibility by providing activityType as a comma-joined string
    const payload = { location, month, budget, activityType: activities.join(','), activities }
    onCreate && onCreate(payload)
  }

  const addActivity = (word) => {
    const clean = (word || '').trim()
    if (!clean) return
    // only allow single words (no spaces)
    if (clean.split(/\s+/).length > 1) return
    // prevent duplicates
    if (activities.includes(clean)) return
    setActivities(prev => [...prev, clean])
  }

  const removeActivity = (idx) => {
    setActivities(prev => prev.filter((_, i) => i !== idx))
  }

  const handleActivityKeyDown = (e) => {
    if (e.key === 'Enter'){
      e.preventDefault()
      if (!activityInput) return
      addActivity(activityInput)
      setActivityInput('')
    }
    if (e.key === 'Backspace' && !activityInput && activities.length){
      // remove last activity on backspace when input empty
      removeActivity(activities.length - 1)
    }
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
        <div className="relative bg-white/95 p-6 md:p-8 rounded-2xl shadow-2xl text-left backdrop-blur-sm">
          <h1 className="text-7xl font-extrabold mb-4 py-4 text-center text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-pink-500">Daycation</h1>
          <form onSubmit={handleSubmit} className="space-y-4 text-left">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

              <label className="block">
                <span className="text-sm font-medium text-slate-700">Location</span>
                <input value={location} onChange={e=>setLocation(e.target.value)} className="mt-1 block w-full p-3 border border-transparent rounded-lg shadow-sm" placeholder="e.g. Bora Bora" />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-slate-700">Month</span>
                <select value={month} onChange={e=>setMonth(e.target.value)} className="mt-1 block w-full p-3 border border-transparent rounded-lg shadow-sm bg-white">
                  <option value="">Select month</option>
                  <option value="January">January</option>
                  <option value="February">February</option>
                  <option value="March">March</option>
                  <option value="April">April</option>
                  <option value="May">May</option>
                  <option value="June">June</option>
                  <option value="July">July</option>
                  <option value="August">August</option>
                  <option value="September">September</option>
                  <option value="October">October</option>
                  <option value="November">November</option>
                  <option value="December">December</option>
                </select>
              </label>

              <label className="block">
                <span className="text-sm font-medium text-slate-700">Budget</span>
                <div className="mt-2 flex gap-2 flex-wrap">
                  <label className={`flex-1 min-w-0 text-center p-2 rounded-lg border ${budget === '$' ? 'bg-amber-200 border-amber-400' : 'bg-white border-transparent'} cursor-pointer`}>
                    <input type="radio" name="budget" value="$" checked={budget === '$'} onChange={e=>setBudget(e.target.value)} className="sr-only" />
                    <span className="font-semibold">$</span>
                  </label>

                  <label className={`flex-1 min-w-0 text-center p-2 rounded-lg border ${budget === '$$' ? 'bg-amber-200 border-amber-400' : 'bg-white border-transparent'} cursor-pointer`}>
                    <input type="radio" name="budget" value="$$" checked={budget === '$$'} onChange={e=>setBudget(e.target.value)} className="sr-only" />
                    <span className="font-semibold">$$</span>
                  </label>

                  <label className={`flex-1 min-w-0 text-center p-2 rounded-lg border ${budget === '$$$' ? 'bg-amber-200 border-amber-400' : 'bg-white border-transparent'} cursor-pointer`}>
                    <input type="radio" name="budget" value="$$$" checked={budget === '$$$'} onChange={e=>setBudget(e.target.value)} className="sr-only" />
                    <span className="font-semibold">$$$</span>
                  </label>
                </div>
              </label>

            </div>

            {/* Activities row: full width below the grid */}
            <div>
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Activities</span>
                <div className="mt-2 p-2 bg-white rounded-lg border border-transparent shadow-sm">
                  <div className="flex flex-col flex-wrap">

                    <input
                      value={activityInput}
                      onChange={e=>setActivityInput(e.target.value)}
                      onKeyDown={handleActivityKeyDown}
                      className="flex-1 min-w-0 p-2 bg-transparent outline-none text-sm"
                      placeholder="Type a word and press Enter"
                    />
                    <div className='mt-1 gap-1 flex flex-wrap'>
                        {activities.map((a, idx) => (
                        <span key={a + idx} className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-100 text-sm">
                            <span className="capitalize">{a}</span>
                            <button type="button" onClick={()=>removeActivity(idx)} className="text-amber-600 hover:text-amber-800 text-xs font-bold">×</button>
                        </span>
                        ))}  
                    </div>
                    
                  </div>
                </div>
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
