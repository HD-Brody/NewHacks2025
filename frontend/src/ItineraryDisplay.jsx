import React from 'react'

export default function ItineraryDisplay({ itinerary }){
  if (!itinerary || itinerary.length === 0) return <div>No itinerary to display</div>

  return (
    <div className="space-y-4">
      {itinerary.map((item, idx) => (
        <div key={idx} className="p-3 border rounded">
          <div className="font-semibold">{item.place}</div>
          <div className="text-sm text-gray-600">{item.start_time} - {item.end_time}</div>
          <div className="text-sm mt-1">{item.notes}</div>
          {item.coordinates && (
            <div className="text-xs text-gray-500 mt-1">coords: {item.coordinates.lat}, {item.coordinates.lng}</div>
          )}
        </div>
      ))}
    </div>
  )
}
