import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The FastAPI app (uvicorn on :8000 locally, the Python function on Vercel) serves these routes
const API_ROUTES = ['/batteries', '/optimization'];

export default defineConfig({
  plugins: [react()],
  build: {
    // Vercel serves ../public as static files next to the FastAPI function
    outDir: '../public',
    emptyOutDir: true,
  },
  server: {
    // `npm run dev` forwards API calls to a local uvicorn
    proxy: Object.fromEntries(API_ROUTES.map(route => [route, 'http://127.0.0.1:8000'])),
  },
});
