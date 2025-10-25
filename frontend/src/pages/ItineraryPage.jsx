import React from 'react'
import ItineraryDisplay from '../ItineraryDisplay'
import MapView from '../MapView'

export default function ItineraryPage({ formData = {}, itinerary = [], onBack, setItinerary }){
  return (
    <div className="min-h-screen min-w-full flex flex-col">
      <div className="flex items-center justify-between p-4 bg-white border-b">
        <div className="flex items-center gap-3">
          <button onClick={onBack} className="px-3 py-1 bg-gray-100 rounded">Back</button>
          <div>
            <div className="text-sm text-gray-500">Trip</div>
            <div className="font-semibold">{formData.location || 'Untitled trip'}</div>
          </div>
        </div>
        <div className="text-sm text-gray-600">{formData.month ? `${formData.month}` : ''} {formData.budget ? `• $${formData.budget}` : ''}</div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        <div className="w-1/2 h-full overflow-auto p-6 bg-white">
          <h2 className="text-lg font-medium mb-4">Itinerary</h2>
          <ItineraryDisplay itinerary={itinerary} />
        </div>
        <div className="w-1/2 h-full overflow-auto p-6 bg-gray-50 border-l">
          <h2 className="text-lg font-medium mb-4">Map</h2>
          <MapView itinerary={itinerary} />
        </div>
      </div>
    </div>
  )
}
