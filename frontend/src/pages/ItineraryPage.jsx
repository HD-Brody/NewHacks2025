import React from 'react'
import ItineraryDisplay from '../ItineraryDisplay'
import MapView from '../MapView'

export default function ItineraryPage({ formData = {}, itinerary = [], onBack, setItinerary }){
  return (
    <div className="relative flex flex-col min-h-screen px-0 bg-gradient-to-b from-yellow-100 via-amber-50 to-sky-50 overflow-hidden">

      {/* Header — full width, sits at the top */}
      <div className="flex items-center justify-between p-6">
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
      <div className="flex-1 flex overflow-hidden">
        <div className="w-1/2 h-full overflow-auto p-6">
          <h2 className="text-lg font-medium mb-4 text-slate-700">Itinerary</h2>
          <div className="h-full">
            <ItineraryDisplay itinerary={itinerary} />
          </div>
        </div>

        <div className="w-1/2 h-full overflow-auto p-6 border-l border-sky-100">
          <h2 className="text-lg font-medium mb-4 text-slate-700">Map</h2>
          <div className="h-full">
            <MapView itinerary={itinerary} />
          </div>
        </div>
      </div>
    </div>
  )
}
