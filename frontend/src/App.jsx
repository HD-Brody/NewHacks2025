import React, { useState } from 'react'
import LandingPage from './pages/LandingPage'
import ItineraryPage from './pages/ItineraryPage'
import { useEffect } from 'react'
import { fetchItinerary } from './api' // adjust path if needed

export function useItineraryFetcher(formData, setItinerary) {
  useEffect(() => {
    // guard: make sure formData has the required fields
    if (!formData.destination || !formData.month || !formData.preferences?.length) return

    let cancelled = false

    const fetchData = async () => {
      try {
        const payload = {
          destination: formData.destination,
          month: formData.month,
          preferences: formData.preferences,
        }

        const result = await fetchItinerary(payload)
        if (cancelled) return

        setItinerary(result.itinerary || [])
      } catch (error) {
        console.error('Error fetching itinerary:', error)
      }
    }

    fetchData()
    return () => { cancelled = true }
  }, [formData.destination, formData.month, formData.preferences, setItinerary])
}

// Simple in-app routing between 'landing' and 'itinerary' pages.
export default function App(){
  const [route, setRoute] = useState('landing') // 'landing' | 'itinerary'
  const [formData, setFormData] = useState({})
  const [itinerary, setItinerary] = useState([])

  const handleCreate = (data) => {
    setFormData(data)
    // For now we keep itinerary empty until backend returns results.
    // In many apps you'd call the API here and populate `itinerary`.
    setItinerary([])
    setRoute('itinerary')
  }

  const handleBack = () => setRoute('landing')

  return (
    <div className="min-h-screen bg-gray-50">
      {route === 'landing' ? (
        <LandingPage
          initial={formData}
          onCreate={handleCreate}
        />
      ) : (
        <ItineraryPage
          formData={formData}
          itinerary={itinerary}
          onBack={handleBack}
          setItinerary={setItinerary}
        />
      )}
    </div>
  )
}
