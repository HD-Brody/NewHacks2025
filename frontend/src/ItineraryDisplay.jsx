import React from 'react'

export default function ItineraryDisplay({ itinerary }){
  if (!itinerary || itinerary.length === 0) return <div>No itinerary to display</div>

  const fmtPrice = (p) => {
    if (p == null || p === '') return '—'
    if (typeof p === 'number') return `$${p}`
    return String(p)
  }

  return (
    <div>
      <ol className="list-decimal space-y-3 pl-6">
        {itinerary.map((item, idx) => {
          // Normalize and format time values coming from different generators
          let time = ''
          if (Array.isArray(item.time) && item.time.length === 2) {
            time = `${item.time[0]} - ${item.time[1]}`
          } else if (typeof item.time === 'string' && item.time.trim()) {
            time = item.time
          } else if (item.start_time || item.end_time) {
            const s = item.start_time || item.start || ''
            const e = item.end_time || item.end || ''
            time = s && e ? `${s} - ${e}` : (s || e || '')
          } else if (item.start || item.end) {
            time = item.start && item.end ? `${item.start} - ${item.end}` : (item.start || item.end || '')
          }

          // Title may be under several keys depending on generator output
          const title = item.title || item.place || item.name || 'Untitled activity'
          const category = item.category || item.type || 'General'
          const price = fmtPrice(item.price || item.cost)
          const description = item.description || item.notes || ''

          return (
            <li key={idx} className="p-3 bg-white/95 rounded-2xl shadow-lg border rounded">
              <div className="flex items-baseline justify-between">
                <div className="font-semibold text-lg">{title}</div>
                <div className="text-sm text-gray-600">{time}</div>
              </div>
              <div className="text-sm text-gray-500 mt-1">Category: <span className="text-gray-700">{category}</span> · Price: <span className="text-gray-700">{price}</span></div>
              {description && <div className="text-sm mt-2">{description}</div>}
              {item.coordinates && (
                <div className="text-xs text-gray-500 mt-2">coords: {item.coordinates.lat}, {item.coordinates.lng}</div>
              )}
            </li>
          )
        })}
      </ol>
    </div>
  )
}
