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
// For testing we hardcode a sample itinerary object and convert it
// into the array shape the UI expects.
export default function App(){
  // Hardcoded test itinerary (matches the user's provided object)
  const TEST_ITINERARY_OBJ = {
  "Places": {
    "Colosseum": {
      "time": ["09:00", "11:00"],
      "category": "historical site",
      "price": "$$",
      "description": "Explore the iconic ancient Roman amphitheater, a symbol of Rome's grandeur and engineering."
    },
    "Roman Forum": {
      "time": ["11:00", "12:30"],
      "category": "historical site",
      "price": "$$",
      "description": "Wander through the ruins of ancient government buildings, temples, and basilicas next to the Colosseum."
    },
    "Trattoria Da Enzo al 29": {
      "time": ["13:00", "14:30"],
      "category": "food",
      "price": "$$",
      "description": "Enjoy authentic Roman cuisine and traditional dishes at a beloved trattoria in Trastevere."
    },
    "Santa Maria in Trastevere": {
      "time": ["14:45", "15:45"],
      "category": "church",
      "price": "$",
      "description": "Visit one of Rome's oldest churches, famous for its stunning mosaics and peaceful ambiance."
    },
    "Gelateria Otaleg": {
      "time": ["16:00", "16:45"],
      "category": "food",
      "price": "$",
      "description": "Indulge in artisanal, high-quality gelato with unique and classic flavors."
    },
    "Gianicolo Hill": {
      "time": ["17:00", "18:00"],
      "category": "outdoor",
      "price": "$",
      "description": "Enjoy panoramic views of Rome, offering a perfect spot for sunset over the city."
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
