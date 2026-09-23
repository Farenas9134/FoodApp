import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] })
  ],
  // Ensures any incoming requests that have a URL that start with /api
  // have to be forwarded to http://localhost:5000 which is where Flask is running
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        // strips '/api' prefix
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
