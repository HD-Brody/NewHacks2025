import React, { useState } from 'react'
import { fetchItinerary } from './api'

export default function ItineraryForm({ onResult }){
  const [destination, setDestination] = useState('')
  const [month, setMonth] = useState('')
  const [preferences, setPreferences] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    const prefs = preferences.split(',').map(s => s.trim()).filter(Boolean)
    try {
      const data = await fetchItinerary({ destination, month, preferences: prefs })
      // TODO: handle errors in response
      onResult && onResult(data.itinerary || [])
    } catch (err) {
      console.error('Failed to fetch itinerary', err)
      onResult && onResult([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium">Destination</label>
        <input value={destination} onChange={e=>setDestination(e.target.value)} className="mt-1 block w-full" placeholder="e.g. Paris" />
      </div>
      <div>
        <label className="block text-sm font-medium">Month (optional)</label>
        <input value={month} onChange={e=>setMonth(e.target.value)} className="mt-1 block w-full" placeholder="e.g. July" />
      </div>
      <div>
        <label className="block text-sm font-medium">Preferences (comma-separated)</label>
        <input value={preferences} onChange={e=>setPreferences(e.target.value)} className="mt-1 block w-full" placeholder="e.g. museums, hiking" />
      </div>
      <div>
        <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded" disabled={loading}>{loading ? 'Generating...' : 'Generate Itinerary'}</button>
      </div>
    </form>
  )
}
