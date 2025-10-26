import React, { useState } from 'react'
import LandingPage from './pages/LandingPage'
import ItineraryPage from './pages/ItineraryPage'

// Simple in-app routing between 'landing' and 'itinerary' pages.
// For testing we hardcode a sample itinerary object and convert it
// into the array shape the UI expects.
export default function App(){
  // Hardcoded test itinerary (matches the user's provided object)
  const TEST_ITINERARY_OBJ = {
    Places: {
      "Meiji Jingu Shrine": {
        "time": ["10:00", "11:30"],
        "category": "outdoor",
        "price": "$",
        "description": "Explore a vast, serene forest shrine dedicated to Emperor Meiji."
      },
      "Wagyu Beef Yakiniku Lunch": {
        "time": ["12:30", "14:00"],
        "category": "food",
        "price": "$$",
        "description": "Savor a high-quality Wagyu beef set meal at a specialized yakiniku restaurant."
      },
      "Tokyo Metropolitan Government Building Observation Decks": {
        "time": ["14:30", "15:30"],
        "category": "outdoor",
        "price": "$",
        "description": "Enjoy free panoramic views of Tokyo from a skyscraper observation deck."
      },
      "Shinjuku Gyoen National Garden": {
        "time": ["16:00", "17:30"],
        "category": "outdoor",
        "price": "$",
        "description": "Stroll through a beautiful fusion of Japanese, English, and French landscape gardens."
      },
      "Omoide Yokocho (Memory Lane)": {
        "time": ["18:30", "20:00"],
        "category": "food",
        "price": "$$",
        "description": "Experience a retro alleyway with tiny izakayas offering grilled skewers and drinks."
      }
    }
  }

  // Helper to turn numeric times like 10.00 or 11.3 into "HH:MM"
  const formatTime = (t) => {
    if (t == null) return ''
    if (typeof t === 'string') return t
    const hours = Math.floor(t)
    const minutes = Math.round((t - hours) * 60)
    const mm = String(minutes).padStart(2, '0')
    return `${hours}:${mm}`
  }

  // Convert the Places object into an array the UI components expect
  const convert = (obj) => {
    if (!obj || !obj.Places) return []
    return Object.entries(obj.Places).map(([name, info]) => {
      const timeArr = info.time || []
      const time = (Array.isArray(timeArr) && timeArr.length === 2)
        ? `${formatTime(timeArr[0])} - ${formatTime(timeArr[1])}`
        : (info.time || '')

      return {
        title: name,
        time,
        category: info.category,
        price: info.price,
        description: info.description
      }
    })
  }

  const TEST_ITINERARY = convert(TEST_ITINERARY_OBJ)

  const [route, setRoute] = useState('landing') // 'landing' | 'itinerary'
  const [formData, setFormData] = useState({})
  // Initialize itinerary with the hardcoded test data for easy testing
  const [itinerary, setItinerary] = useState(TEST_ITINERARY)

  const handleCreate = (data) => {
    setFormData(data)
    // For testing we set the hardcoded itinerary
    setItinerary(TEST_ITINERARY)
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
