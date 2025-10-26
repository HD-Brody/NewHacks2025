import React, {useEffect} from 'react'
import ItineraryDisplay from '../ItineraryDisplay'
import MapView from '../MapView'
import { fetchGeocode } from '../api'

export default function ItineraryPage({ formData = {}, itinerary = [], onBack, setItinerary }){
  useEffect(() => {
    if (!itinerary || itinerary.length === 0) return
    const needsCoords = itinerary.some(item => !item.coordinates)
    if (!needsCoords) return

    let cancelled = false

    // Fetch geocode data when the component mounts
    const fetchGeocodeData = async () => {
      try {
        const places = itinerary.map(item => item.title).filter(Boolean)
        const coordsMap = await fetchGeocode({ places, location: formData.location, country: formData.country })

        if (cancelled) return
        setItinerary(prev => prev.map(item => ({
          ...item,
          coordinates: item.coordinates || coordsMap[item.title] || null
        })))
      } catch (error) {
        console.error('Error fetching geocode data:', error)
      }
    }

    fetchGeocodeData()
    return () => { cancelled = true }
  }, [formData.location, formData.country, itinerary.length, setItinerary])

  return (
    <div className="relative flex flex-col h-screen px-0 bg-gradient-to-b from-yellow-100 via-amber-50 to-sky-50 overflow-hidden">

      {/* Header — full width, sits at the top */}
      <div className="flex items-center justify-between p-6 shadow-lg">
        <div className="flex items-center gap-4">
          <button onClick={onBack} className="px-4 py-2 bg-amber-100 hover:bg-amber-200 rounded-full shadow-sm">Back</button>
          <div>
            <div className="text-sm text-slate-600">Trip</div>
            <div className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-pink-500">{formData.location || 'Untitled trip'}</div>
          </div>
        </div>

        <div className="text-sm text-slate-600">{formData.month ? `${formData.month}` : ''} {formData.budget ? `• ${formData.budget}` : ''}</div>
      </div>

      {/* Main content — take remaining height and split into two columns */}
      <div className="flex-1 flex overflow-hidden min-h-0">
        <div className="w-1/2 overflow-auto p-6 min-h-0">
          <h2 className="text-lg font-medium mb-4 text-slate-700">Itinerary</h2>
          <div className="min-h-0">
            <ItineraryDisplay itinerary={itinerary} />
          </div>
        </div>

        <div className="w-1/2 overflow-auto border-l border-sky-100 min-h-0">
          <div className="h-full min-h-0">
            <MapView itinerary={itinerary} />
          </div>
        </div>
      </div>
    </div>
  )
}
