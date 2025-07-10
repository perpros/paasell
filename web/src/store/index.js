import { defineStore } from 'pinia';
import apiClient from '@/services/api'; // apiClient for making API calls
import router from '@/router'; // Import router for navigation

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null, // User object might contain id, username, email, roles
    status: { loggedIn: !!localStorage.getItem('token') }, // Simple status
    loginError: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
    getToken: (state) => state.token,
    isAdmin: (state) => state.user && state.user.roles && state.user.roles.some(role => role.name === 'Admin'),
    // Add more role checks if needed e.g. isSupplier, isSupport
  },
  actions: {
    async login(credentials) {
      this.loginError = null;
      try {
        // FastAPI's OAuth2PasswordRequestForm expects form data
        const formData = new FormData();
        formData.append('username', credentials.username); // 'username' is the key expected by OAuth2PasswordRequestForm
        formData.append('password', credentials.password);

        const response = await apiClient.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });

        const { access_token } = response.data;
        this.token = access_token;
        localStorage.setItem('token', access_token);

        // After successful login, fetch user details using the new token
        // The /users/me endpoint should return current user's details including roles
        const userResponse = await apiClient.get('/users/me'); // apiClient will use the new token from interceptor
        this.user = userResponse.data; // Assuming response.data is the user object {id, username, email, roles: [{name}]}
        localStorage.setItem('user', JSON.stringify(this.user));

        this.status.loggedIn = true;
        return true; // Indicate successful login
      } catch (error) {
        this.status.loggedIn = false;
        this.token = null;
        this.user = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        if (error.response && error.response.data && error.response.data.detail) {
          this.loginError = error.response.data.detail;
        } else {
          this.loginError = 'Login failed. Please try again.';
        }
        console.error('Login error:', error);
        return false; // Indicate failed login
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      this.status.loggedIn = false;
      this.loginError = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      // Optional: Call a backend /auth/logout endpoint if it exists
      // apiClient.post('/auth/logout');
      router.push('/login'); // Redirect to login page
    },
    // Action to initialize store from localStorage (e.g., on app load)
    // This is implicitly handled by state definition, but an explicit action can be useful.
    hydrateAuth() {
      this.token = localStorage.getItem('token') || null;
      this.user = JSON.parse(localStorage.getItem('user')) || null;
      this.status.loggedIn = !!this.token;
    },
    // Utility to update user data if needed (e.g., after profile update)
    updateUser(userData) {
        this.user = { ...this.user, ...userData };
        localStorage.setItem('user', JSON.stringify(this.user));
    }
  },
});
