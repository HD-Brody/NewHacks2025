import React, { useState } from 'react'
import ItineraryForm from './ItineraryForm'
import ItineraryDisplay from './ItineraryDisplay'
import MapView from './MapView'

export default function App(){
  const [itinerary, setItinerary] = useState([])

  return (
    <div className="min-h-screen bg-gray-50 flex items-start justify-center py-10">
      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 p-6 bg-white rounded shadow">
          <h1 className="text-xl font-semibold mb-4">Generate Itinerary</h1>
          <ItineraryForm onResult={setItinerary} />
        </div>
        <div className="md:col-span-2 space-y-6">
          <div className="p-6 bg-white rounded shadow">
            <h2 className="text-lg font-medium mb-2">Planned Stops</h2>
            <ItineraryDisplay itinerary={itinerary} />
          </div>
          <div className="p-6 bg-white rounded shadow">
            <h2 className="text-lg font-medium mb-2">Map</h2>
            <MapView itinerary={itinerary} />
          </div>
        </div>
      </div>
    </div>
  )
}
