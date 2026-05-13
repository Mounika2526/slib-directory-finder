/**
 * main.jsx — Application entry point for SLIB Finder
 *
 * Mounts the root React component into the DOM element with id="root".
 * StrictMode is enabled to highlight potential issues during development.
 * Tailwind CSS is loaded globally via index.css.
 */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)