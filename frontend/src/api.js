export async function fetchItinerary(payload){
  // payload: { destination, month, preferences }
  // TODO: add proper error handling, timeouts, and auth if needed
  const res = await fetch('/api/generate_itinerary', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`API Error ${res.status}: ${text}`)
  }
  return res.json()
}

export async function fetchGeocode({ places = [], location = '', country = '' } = {}) {
  const res = await fetch('/api/geocode', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ places, location, country })
  })
  if (!res.ok) {
    // include response body (if any) in the thrown error to aid debugging
    let body
    try {
      body = await res.text()
    } catch (e) {
      body = '<unreadable response body>'
    }
    throw new Error(`Geocode API error ${res.status}: ${body}`)
  }
  return res.json() // expected: { "Place A": {lat, lng}, ... }
}

export async function fetchPolylines(payload){
  // payload: { itinerary: [...]} or { pairs: [...] }
  const res = await fetch('/api/route_polylines', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!res.ok) {
    let body
    try { body = await res.text() } catch (e) { body = '<unreadable response>' }
    throw new Error(`Route API error ${res.status}: ${body}`)
  }
  return res.json()
}