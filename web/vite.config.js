import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), '')
  return {
    plugins: [
      vue(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      host: true, // Listen on all addresses, including LAN and public addresses
      port: 5173, // Default Vite port
      proxy: {
        // Proxy API requests to backend during development
        // Any request to /api will be forwarded to http://localhost:8000/api
        // This should match the API_V1_STR in the backend
        [env.VITE_API_PROXY_PREFIX || '/api/v1']: {
          target: env.VITE_API_PROXY_TARGET || 'http://backend:8000', // Target backend, 'backend' is the service name in docker-compose
          changeOrigin: true,
          // rewrite: (path) => path.replace(new RegExp(`^${env.VITE_API_PROXY_PREFIX || '/api/v1'}`), ''), // if backend doesn't expect /api/v1 prefix
        }
      }
    },
    define: {
      // Vite replaces these strings in the client-side code at build time.
      'process.env.VITE_API_BASE_URL': JSON.stringify(env.VITE_API_BASE_URL || '/api/v1'),
    },
    test: { // Vitest configuration
      globals: true,
      environment: 'jsdom',
      setupFiles: './src/testSetup.js', // if you need setup files
    }
  }
})
