import React, { useState } from 'react'

export default function LandingPage({ initial = {}, onCreate }){
  const [location, setLocation] = useState(initial.location || '')
  const [month, setMonth] = useState(initial.month || '')
  const [budget, setBudget] = useState(initial.budget || '')
  const [activityType, setActivityType] = useState(initial.activityType || '')
  const [customFields, setCustomFields] = useState(initial.customFields || [])

  const addCustomField = () => setCustomFields(prev => [...prev, { key: '', value: '' }])
  const updateCustomField = (idx, key, value) => {
    setCustomFields(prev => prev.map((f,i) => i===idx ? { key, value } : f))
  }
  const removeCustomField = (idx) => setCustomFields(prev => prev.filter((_,i)=>i!==idx))

  const handleSubmit = (e) => {
    e && e.preventDefault()
    const payload = { location, month, budget, activityType, customFields }
    onCreate && onCreate(payload)
  }

  return (
    <div className="flex items-center justify-center min-h-screen px-4">
      <div className="w-full max-w-2xl">
        <div className="text-center">
          <h1 className="text-6xl font-bold mb-6">Perfect Day</h1>
          <form onSubmit={handleSubmit} className="space-y-4 text-left">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <label className="block">
                <span className="text-sm font-medium">Location</span>
                <input value={location} onChange={e=>setLocation(e.target.value)} className="mt-1 block w-full p-2 border rounded" placeholder="e.g. Paris" />
              </label>

              <label className="block">
                <span className="text-sm font-medium">Month</span>
                <input value={month} onChange={e=>setMonth(e.target.value)} className="mt-1 block w-full p-2 border rounded" placeholder="e.g. July" />
              </label>

              <label className="block">
                <span className="text-sm font-medium">Budget</span>
                <input value={budget} onChange={e=>setBudget(e.target.value)} className="mt-1 block w-full p-2 border rounded" placeholder="e.g. 1500" />
              </label>

              <label className="block">
                <span className="text-sm font-medium">Activity type</span>
                <input value={activityType} onChange={e=>setActivityType(e.target.value)} className="mt-1 block w-full p-2 border rounded" placeholder="e.g. museums, hiking" />
              </label>

              {/* <div className="md:col-span-2 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Custom fields</span>
                  <button type="button" onClick={addCustomField} className="text-sm text-blue-600">Add</button>
                </div>
                {customFields.map((f, idx) => (
                  <div key={idx} className="flex gap-2">
                    <input value={f.key} onChange={e=>updateCustomField(idx, e.target.value, f.value)} placeholder="key" className="flex-1 p-2 border rounded" />
                    <input value={f.value} onChange={e=>updateCustomField(idx, f.key, e.target.value)} placeholder="value" className="flex-1 p-2 border rounded" />
                    <button type="button" onClick={()=>removeCustomField(idx)} className="px-3 py-2 bg-red-100 text-red-700 rounded">×</button>
                  </div>
                ))}
              </div> */}
            </div>

            <div className="text-center pt-4">
              <button type="submit" className="px-6 py-3 bg-blue-600 text-white rounded">Create Itinerary</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
