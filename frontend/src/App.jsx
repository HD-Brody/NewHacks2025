import React, {useEffect, useState} from 'react'

export default function App(){
  const [msg, setMsg] = useState('Loading...')

  useEffect(()=>{
    fetch('/api/hello')
      .then(r => r.json())
      .then(d => setMsg(d.message))
      .catch(()=> setMsg('Failed to reach backend'))
  },[])

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-lg p-8 bg-white rounded shadow">
        <h1 className="text-2xl font-semibold mb-4">NewHacks2025</h1>
        <p className="text-gray-700">Backend says: <strong>{msg}</strong></p>
      </div>
    </div>
  )
}
