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
