import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store'; // Import Pinia auth store

// View Components
import LoginView from '../views/LoginView.vue'
// Example: Create a DashboardView for a protected route
// import DashboardView from '../views/DashboardView.vue'
// For now, let's create a simple placeholder for a protected "Home" or "Dashboard"
const HomeView = { template: '<div><h1>Welcome!</h1><p>You are logged in.</p><button @click="logout">Logout</button></div>', methods: { logout() { useAuthStore().logout(); }} };
const AdminAreaView = { template: '<div><h1>Admin Area</h1><p>Only admins can see this.</p></div>' };


const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guest: true } // For redirecting logged-in users from login page
  },
  {
    path: '/',
    name: 'home',
    component: HomeView, // Replace with your actual home/dashboard component
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard', // Example protected route
    name: 'dashboard',
    component: HomeView, // Using HomeView as placeholder
    meta: { requiresAuth: true }
  },
  {
    path: '/admin', // Example admin-only route
    name: 'admin',
    component: AdminAreaView, // Placeholder for an admin component
    meta: { requiresAuth: true, roles: ['Admin'] } // Specify required roles
  }
  // Add other routes here
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // Ensure Pinia store is hydrated, especially on first load/refresh
  // This might be better handled in main.js or App.vue on app initialization
  if (!authStore.status.loggedIn && localStorage.getItem('token')) {
    authStore.hydrateAuth(); // Attempt to rehydrate from localStorage
  }

  const isAuthenticated = authStore.isAuthenticated;
  const requiredRoles = to.meta.roles;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      // Not authenticated, redirect to login page
      next({
        name: 'login',
        query: { redirect: to.fullPath } // Save the intended path
      });
    } else {
      // Authenticated. Check for role authorization if 'roles' meta field is present
      if (requiredRoles && requiredRoles.length > 0) {
        const userRoles = authStore.currentUser?.roles?.map(role => role.name) || [];
        const hasRequiredRole = requiredRoles.some(role => userRoles.includes(role));

        if (hasRequiredRole) {
          next(); // User has the required role
        } else {
          // User does not have the required role
          // Redirect to a 'Forbidden' page or home. For now, redirect to home.
          // You might want to create a specific '403 Forbidden' view.
          alert("You don't have permission to access this page."); // Simple feedback
          next({ name: 'home' });
        }
      } else {
        next(); // No specific roles required, just authentication
      }
    }
  } else if (to.matched.some(record => record.meta.guest) && isAuthenticated) {
    // If user is authenticated and tries to access a 'guest' page (like login)
    // redirect them to the home page or dashboard.
    next({ name: 'home' });
  }
  else {
    next(); // No auth meta, proceed
  }
});

export default router
