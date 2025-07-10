import axios from 'axios';
import { useAuthStore } from '@/store/auth'; // Import Pinia store

// Get the base URL from environment variables
// Vite provides import.meta.env.VITE_API_BASE_URL for client-side code
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    // 'X-Requested-With': 'XMLHttpRequest', // Often good for identifying AJAX requests
  },
});

// Request interceptor to add JWT token to headers
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore(); // Access store inside interceptor
    const token = authStore.getToken;
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor (optional, can be used for global error handling, e.g. 401 to logout)
apiClient.interceptors.response.use(
  (response) => {
    // Any status code that lie within the range of 2xx cause this function to trigger
    return response;
  },
  (error) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      // Only clear auth data if it's not a login failure (to avoid loops)
      // This needs careful handling based on which endpoint returned 401
      // For example, if /auth/login returns 401, we don't want to immediately logout.
      // A common practice is to have a specific error code or header for "invalid token" vs "invalid credentials".
      console.error('Unauthorized request or token expired. Logging out.');
      authStore.clearAuthData();
      // Redirect to login page - this might be better handled in router navigation guards
      // or by the component making the call.
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
