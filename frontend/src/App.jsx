import React, { useState } from 'react'
import LandingPage from './pages/LandingPage'
import ItineraryPage from './pages/ItineraryPage'
import { useEffect } from 'react'
import { fetchItinerary } from './api' // adjust path if needed

export function useItineraryFetcher(formData, setItinerary) {
  useEffect(() => {
    // guard: accept either `destination` or `location`, and various preference shapes
    const destination = formData.destination || formData.location
    const month = formData.month
    const preferences = formData.preferences || formData.activities || (formData.activityType ? formData.activityType.split(',').map(s=>s.trim()).filter(Boolean) : [])
    if (!destination || !month || !preferences.length) return

    let cancelled = false

    const fetchData = async () => {
      try {
        const payload = {
          destination,
          month,
          preferences,
          budget: formData.budget || formData.price || null,
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
  }, [formData, setItinerary])
}

// Simple in-app routing between 'landing' and 'itinerary' pages.
export default function App(){
  /*
  Hardcoded test itinerary (kept for reference). Commented out so the app
  fetches real itinerary data from the backend instead. To re-enable the
  hardcoded example, uncomment the block below.

  const TEST_ITINERARY_OBJ = { ... }
  const TEST_ITINERARY = convert(TEST_ITINERARY_OBJ)
  */

  const [route, setRoute] = useState('landing') // 'landing' | 'itinerary'
  const [formData, setFormData] = useState({})
  // Initialize itinerary empty — we'll fetch it from the backend
  const [itinerary, setItinerary] = useState([])

  // Kick off fetching when formData changes (the hook is defined above)
  useItineraryFetcher(formData, setItinerary)

  const handleCreate = (data) => {
    // Save form data and navigate to the Itinerary page. The
    // `useItineraryFetcher` hook will detect the updated formData and
    // request the generated itinerary from the backend.
    setFormData(data)
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
