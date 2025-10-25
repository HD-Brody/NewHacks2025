import React, { useState } from 'react'
import LandingPage from './pages/LandingPage'
import ItineraryPage from './pages/ItineraryPage'

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
