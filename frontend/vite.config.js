/**
 * vite.config.js — Vite build configuration for SLIB Finder frontend
 *
 * Plugins:
 *   react()      — enables JSX transform and React Fast Refresh in dev mode
 *   tailwindcss() — processes Tailwind utility classes at build time
 */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});