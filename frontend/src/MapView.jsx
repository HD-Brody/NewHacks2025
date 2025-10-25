import React, { useMemo, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix default icon URLs for Vite bundler (ensures marker images load)
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
})

function FitBounds({ bounds }) {
  const map = useMap()
  useEffect(() => {
    if (!map || !bounds || bounds.length === 0) return
    map.fitBounds(bounds, { padding: [40, 40] })
  }, [map, bounds])
  return null
}

export default function MapView({ itinerary, initialCenter = [41.886954, 12.501652], initialZoom = 13 }) {
  // itinerary expected to be an array of items with { place, coordinates: { lat, lng } }
  const points = (itinerary || []).map(i => ({ place: i.place, coords: i.coordinates }))

  const hasCoords = points.some(p => p.coords && p.coords.lat != null && p.coords.lng != null)

  const bounds = points
    .filter(p => p.coords && p.coords.lat != null && p.coords.lng != null)
    .map(p => [p.coords.lat, p.coords.lng])

  const center = useMemo(() => (bounds && bounds.length ? bounds[0] : initialCenter), [bounds, initialCenter])

  return (
    <div className="h-full w-full">
      <MapContainer
        center={center}
        zoom={initialZoom}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/">CARTO</a> contributors'
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />

        {points.map((p, idx) => (
          p.coords && (
            <Marker key={idx} position={[p.coords.lat, p.coords.lng]}>
              <Popup>
                <div className="font-semibold">{p.place}</div>
                <div className="text-xs">{p.coords.lat}, {p.coords.lng}</div>
              </Popup>
            </Marker>
          )
        ))}

        <FitBounds bounds={bounds} />
      </MapContainer>
    </div>
  )
}
