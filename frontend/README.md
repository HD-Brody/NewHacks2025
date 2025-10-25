# Frontend — dependencies & setup

This folder contains the Vite + React + Tailwind frontend.

Notable dependencies (from `package.json`):
- react ^18.2.0
- react-dom ^18.2.0
- leaflet ^1.9.x
- react-leaflet ^4.x
- mapbox-gl ^3.x
- Tailwind / Vite dev tooling in `devDependencies`

Quick setup (PowerShell):

```powershell
cd frontend
npm install
npm run dev
```

Notes:
- The frontend dev server usually runs at `http://localhost:5173`.
- The app calls `/api/*` routes; run the backend first so `/api` routes respond.
- If you see peer-dependency warnings, try `npm install --legacy-peer-deps` as a fallback.
- If using Leaflet, import its CSS in your components:

```js
import 'leaflet/dist/leaflet.css'
```
