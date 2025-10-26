import React, { useMemo, useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap, Polyline } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { fetchPolylines } from './api'

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

export default function MapView({ itinerary = [], initialCenter = [35.68, 139.76], initialZoom = 11 }) {
  // itinerary expected to be an array of items with { title, coordinates: { lat, lng } }
  const points = useMemo(() => (
    (itinerary || [])
      .map(i => {
        if (!i || !i.coordinates || i.coordinates.lat == null || i.coordinates.lng == null) return null
        // Title may be under several keys depending on generator output
        const title = i.title || i.place || i.name || 'Untitled'
        const description = i.description || i.notes || i.summary || ''
        return { title, lat: Number(i.coordinates.lat), lng: Number(i.coordinates.lng), description }
      })
      .filter(Boolean)
  ), [itinerary])

  const bounds = points.map(p => [p.lat, p.lng])
  const center = points.length ? [points[0].lat, points[0].lng] : initialCenter
  const [polylines, setPolylines] = useState([])

  // Fetch polylines for consecutive itinerary points
  useEffect(() => {
    let cancelled = false
    // build simple itinerary payload with coordinates only
    const payloadItin = (itinerary || []).map(item => ({ coordinates: item && item.coordinates ? { lat: Number(item.coordinates.lat), lng: Number(item.coordinates.lng) } : null }))
    const validCount = payloadItin.filter(i => i && i.coordinates && i.coordinates.lat != null && i.coordinates.lng != null).length
    if (validCount < 2) {
      setPolylines([])
      return
    }

    const fetchRoutes = async () => {
      try {
        const res = await fetchPolylines({ itinerary: payloadItin })
        if (cancelled) return
        // pick walk polyline if available, else car
        const lines = (res || []).map(seg => {
          const poly = seg.walk && seg.walk.polyline ? seg.walk.polyline : (seg.car && seg.car.polyline ? seg.car.polyline : null)
          return poly // may be null
        }).filter(Boolean)
        setPolylines(lines)
      } catch (e) {
        console.warn('Failed to fetch polylines', e)
        setPolylines([])
      }
    }

    fetchRoutes()
    return () => { cancelled = true }
  }, [itinerary])

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
          <Marker key={p.title || idx} position={[p.lat, p.lng]}>
            <Popup>
              <div className="font-semibold">{p.title}</div>
              {p.description && <div className="text-sm mt-1">{p.description}</div>}
              <div className="text-xs text-gray-500 mt-1">{p.lat.toFixed(5)}, {p.lng.toFixed(5)}</div>
            </Popup>
          </Marker>
        ))}

        {/* Render polylines between activities */}
        {polylines.map((poly, i) => (
          <Polyline key={`poly-${i}`} positions={poly} pathOptions={{ color: '#1e40af', weight: 4, opacity: 0.9 }} />
        ))}

        {bounds.length > 0 && <FitBounds bounds={bounds} />}
      </MapContainer>
    </div>
  )
}
