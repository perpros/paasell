<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/store'
import { computed } from 'vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isAdmin = computed(() => authStore.isAdmin) // Assuming isAdmin getter exists

const handleLogout = () => {
  authStore.logout()
}
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink v-if="isAuthenticated && isAdmin" to="/admin">Admin Area</RouterLink>
        <RouterLink v-if="!isAuthenticated" to="/login">Login</RouterLink>
        <a href="#" v-if="isAuthenticated" @click.prevent="handleLogout">Logout</a>
      </nav>
      <div v-if="isAuthenticated && authStore.currentUser" class="user-info">
        Logged in as: {{ authStore.currentUser.username }} ({{ authStore.currentUser.roles.map(r => r.name).join(', ') }})
      </div>
    </div>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style scoped>
header {
  background-color: #f8f9fa;
  padding: 1rem 2rem;
  border-bottom: 1px solid #e0e0e0;
  line-height: 1.5;
}

.wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

nav {
  display: flex;
  gap: 1rem; /* Space between nav items */
}

nav a {
  text-decoration: none;
  color: #007bff;
  padding: 0.5rem 0;
  font-weight: 500;
}

nav a.router-link-exact-active {
  color: #0056b3;
  border-bottom: 2px solid #0056b3;
}

nav a:hover {
  color: #0056b3;
}

.user-info {
  font-size: 0.9rem;
  color: #555;
}

main {
  padding: 1rem;
}

/* Responsive adjustments if needed */
@media (max-width: 768px) {
  .wrapper {
    flex-direction: column;
    align-items: flex-start;
  }
  nav {
    margin-bottom: 0.5rem;
    width: 100%;
    justify-content: center; /* Center nav items on smaller screens */
  }
  .user-info {
    margin-top: 0.5rem;
    text-align: center;
    width: 100%;
  }
}
</style>
