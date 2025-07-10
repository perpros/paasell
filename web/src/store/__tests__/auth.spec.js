import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '@/store'; // Imports from store/index.js
import apiClient from '@/services/api';
import router from '@/router'; // Import router
import { describe, it, expect, beforeEach, vi } from 'vitest';

// Mock apiClient
vi.mock('@/services/api', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

// Mock router
vi.mock('@/router', () => ({
  default: {
    push: vi.fn(),
    currentRoute: { value: { query: {} } } // Mock currentRoute and its query
  }
}));


describe('Pinia Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    // Reset mocks before each test
    apiClient.post.mockReset();
    apiClient.get.mockReset();
    router.push.mockReset();
    // Clear localStorage
    localStorage.clear();
  });

  it('initializes with token and user from localStorage if present', () => {
    localStorage.setItem('token', 'test-token');
    localStorage.setItem('user', JSON.stringify({ id: 1, username: 'testuser', roles: [{name: 'User'}] }));

    const authStore = useAuthStore();

    expect(authStore.isAuthenticated).toBe(true);
    expect(authStore.currentUser).toEqual({ id: 1, username: 'testuser', roles: [{name: 'User'}] });
    expect(authStore.getToken).toBe('test-token');
  });

  it('initializes with null/false if no token in localStorage', () => {
    const authStore = useAuthStore();
    expect(authStore.isAuthenticated).toBe(false);
    expect(authStore.currentUser).toBe(null);
    expect(authStore.getToken).toBe(null);
  });

  describe('login action', () => {
    it('successfully logs in, stores token and user, fetches user details', async () => {
      const authStore = useAuthStore();
      const mockTokenResponse = { data: { access_token: 'new-jwt-token' } };
      const mockUserResponse = { data: { id: 2, username: 'newuser', email: 'new@example.com', roles: [{name: 'Admin'}] } };

      apiClient.post.mockResolvedValueOnce(mockTokenResponse); // For /auth/login
      apiClient.get.mockResolvedValueOnce(mockUserResponse);   // For /users/me

      const credentials = { username: 'newuser', password: 'password' };
      const loginSuccess = await authStore.login(credentials);

      expect(loginSuccess).toBe(true);
      expect(apiClient.post).toHaveBeenCalledTimes(1);
      expect(apiClient.post).toHaveBeenCalledWith('/auth/login', expect.any(FormData), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      const formData = apiClient.post.mock.calls[0][1];
      expect(formData.get('username')).toBe(credentials.username);
      expect(formData.get('password')).toBe(credentials.password);

      expect(apiClient.get).toHaveBeenCalledTimes(1);
      expect(apiClient.get).toHaveBeenCalledWith('/users/me');

      expect(authStore.getToken).toBe('new-jwt-token');
      expect(authStore.currentUser).toEqual(mockUserResponse.data);
      expect(authStore.isAuthenticated).toBe(true);
      expect(localStorage.getItem('token')).toBe('new-jwt-token');
      expect(JSON.parse(localStorage.getItem('user'))).toEqual(mockUserResponse.data);
      expect(authStore.loginError).toBe(null);
    });

    it('handles login failure from API', async () => {
      const authStore = useAuthStore();
      const mockError = {
        response: { data: { detail: 'Invalid credentials' } },
      };
      apiClient.post.mockRejectedValueOnce(mockError);

      const loginSuccess = await authStore.login({ username: 'user', password: 'wrongpassword' });

      expect(loginSuccess).toBe(false);
      expect(authStore.getToken).toBe(null);
      expect(authStore.currentUser).toBe(null);
      expect(authStore.isAuthenticated).toBe(false);
      expect(localStorage.getItem('token')).toBe(null);
      expect(localStorage.getItem('user')).toBe(null);
      expect(authStore.loginError).toBe('Invalid credentials');
    });

    it('handles network or other errors during login', async () => {
        const authStore = useAuthStore();
        apiClient.post.mockRejectedValueOnce(new Error("Network error"));

        const loginSuccess = await authStore.login({ username: 'user', password: 'password' });

        expect(loginSuccess).toBe(false);
        expect(authStore.isAuthenticated).toBe(false);
        expect(authStore.loginError).toBe('Login failed. Please try again.');
      });
  });

  describe('logout action', () => {
    it('clears token and user, and navigates to login', () => {
      // Setup initial logged-in state
      localStorage.setItem('token', 'existing-token');
      localStorage.setItem('user', JSON.stringify({ id: 1, username: 'user' }));
      const authStore = useAuthStore();
      authStore.hydrateAuth(); // Ensure store is hydrated before logout

      expect(authStore.isAuthenticated).toBe(true); // Pre-condition

      authStore.logout();

      expect(authStore.getToken).toBe(null);
      expect(authStore.currentUser).toBe(null);
      expect(authStore.isAuthenticated).toBe(false);
      expect(localStorage.getItem('token')).toBe(null);
      expect(localStorage.getItem('user')).toBe(null);
      expect(router.push).toHaveBeenCalledWith('/login');
    });
  });

  describe('getters', () => {
    it('isAdmin getter works correctly', () => {
      const authStore = useAuthStore();

      // Not logged in
      expect(authStore.isAdmin).toBe(false);

      // Logged in as non-admin
      authStore.user = { id: 1, username: 'user', roles: [{name: 'User'}] };
      expect(authStore.isAdmin).toBe(false);

      // Logged in as admin
      authStore.user = { id: 2, username: 'admin', roles: [{name: 'Admin'}] };
      expect(authStore.isAdmin).toBe(true);

      // Logged in with multiple roles including Admin
      authStore.user = { id: 3, username: 'multiadmin', roles: [{name: 'User'}, {name: 'Admin'}] };
      expect(authStore.isAdmin).toBe(true);

      // Logged in but user.roles is undefined or null
      authStore.user = { id: 4, username: 'norolesuser', roles: undefined };
      expect(authStore.isAdmin).toBe(false);
      authStore.user = { id: 4, username: 'norolesuser', roles: null };
      expect(authStore.isAdmin).toBe(false);
    });
  });

  describe('hydrateAuth action', () => {
    it('correctly hydrates state from localStorage', () => {
        localStorage.setItem('token', 'hydrated-token');
        localStorage.setItem('user', JSON.stringify({ id: 3, username: 'hydrateduser' }));
        const authStore = useAuthStore();
        // Manually set to non-hydrated state first
        authStore.token = null;
        authStore.user = null;
        authStore.status.loggedIn = false;

        authStore.hydrateAuth();

        expect(authStore.getToken).toBe('hydrated-token');
        expect(authStore.currentUser).toEqual({ id: 3, username: 'hydrateduser' });
        expect(authStore.status.loggedIn).toBe(true);
    });
  });
});
