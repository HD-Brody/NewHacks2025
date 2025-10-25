import React from 'react'

export default function MapView({ itinerary }){
  // TODO: integrate with a map library (Leaflet, Mapbox, Google Maps)
  // For now this is a placeholder that lists coordinates when available.
  const points = (itinerary || []).map(i => ({ place: i.place, coords: i.coordinates }))

  return (
    <div className="p-4 border rounded">
      <div className="font-semibold mb-2">Map (placeholder)</div>
      {points.length === 0 && <div className="text-sm text-gray-500">No points to show</div>}
      <ul className="text-sm">
        {points.map((p, idx) => (
          <li key={idx}>{p.place}: {p.coords ? `${p.coords.lat}, ${p.coords.lng}` : 'no coords'}</li>
        ))}
      </ul>
    </div>
  )
}
