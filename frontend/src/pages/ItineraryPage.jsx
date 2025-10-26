import React, { useEffect, useState } from 'react'
import ItineraryDisplay from '../ItineraryDisplay'
import MapView from '../MapView'
import { fetchGeocode } from '../api'

export default function ItineraryPage({ formData = {}, itinerary = [], onBack, setItinerary }){
  const [isRetrying, setIsRetrying] = useState(false)

  const normalize = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[-\uFFFF]/g, '').replace(/[^a-z0-9]+/g, '')
  useEffect(() => {
    if (!itinerary || itinerary.length === 0) return
    const needsCoords = itinerary.some(item => !item.coordinates)
    if (!needsCoords) return

    let cancelled = false

    // Fetch geocode data when the component mounts
    const fetchGeocodeData = async () => {
      try {
        const places = itinerary.map(item => item.title || item.place).filter(Boolean)
        console.log('ItineraryPage: requesting geocode for', places)
        const coordsMap = await fetchGeocode({ places, location: formData.location, country: formData.country })
        console.log('ItineraryPage: coordsMap', coordsMap)

        if (cancelled) return

        // normalize keys from backend and merge into items safely
        const coordsMapNormalized = {}
        Object.entries(coordsMap || {}).forEach(([k, v]) => { coordsMapNormalized[normalize(k)] = v })

        setItinerary(prev => prev.map(item => {
          const key = normalize(item.title || item.place || '')
          const found = coordsMapNormalized[key]
          const coords = found && found.lat != null && found.lng != null
            ? { lat: Number(found.lat), lng: Number(found.lng) }
            : item.coordinates || null
          return { ...item, coordinates: coords }
        }))
      } catch (error) {
        console.error('Error fetching geocode data:', error)
      }
    }

    fetchGeocodeData()
    return () => { cancelled = true }
  }, [formData.location, formData.country, itinerary.length, setItinerary])

  // retry geocoding only for missing items
  const retryMissing = async () => {
    const missing = (itinerary || []).filter(i => !i.coordinates).map(i => i.title || i.place).filter(Boolean)
    if (!missing.length) return
    setIsRetrying(true)
    try {
      console.log('Retrying geocode for missing:', missing)
      const coordsMap = await fetchGeocode({ places: missing, location: formData.location, country: formData.country })
      console.log('Retry coordsMap:', coordsMap)

      const coordsMapNormalized = {}
      Object.entries(coordsMap || {}).forEach(([k, v]) => { coordsMapNormalized[normalize(k)] = v })

      setItinerary(prev => prev.map(item => {
        const key = normalize(item.title || item.place || '')
        if (item.coordinates) return item
        const found = coordsMapNormalized[key]
        const coords = found && found.lat != null && found.lng != null
          ? { lat: Number(found.lat), lng: Number(found.lng) }
          : null
        return { ...item, coordinates: coords }
      }))
    } catch (e) {
      console.error('Retry geocode failed', e)
    } finally {
      setIsRetrying(false)
    }
  }

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
            {/* Show missing coords and allow retry */}
            {Array.isArray(itinerary) && (() => {
              const missing = itinerary.filter(i => !i.coordinates).map(i => i.title || i.place).filter(Boolean)
              if (missing.length > 0) {
                return (
                  <div className="mb-4 p-3 bg-yellow-50 border-l-4 border-yellow-400">
                    <div className="text-sm text-slate-700">No coordinates for: {missing.join(', ')}</div>
                    <div className="mt-2">
                      <button onClick={retryMissing} disabled={isRetrying} className="px-3 py-1 bg-amber-100 hover:bg-amber-200 rounded">
                        {isRetrying ? 'Retrying…' : 'Retry geocode for missing'}
                      </button>
                    </div>
                  </div>
                )
              }
              return null
            })()}

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
