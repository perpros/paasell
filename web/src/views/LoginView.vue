<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username or Email:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/store'; // Auto-imports index.js from store
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  errorMessage.value = '';
  isLoading.value = true;
  try {
    const loginSuccess = await authStore.login({ username: username.value, password: password.value });
    if (loginSuccess) {
      // Redirect to a protected route or home page after successful login
      // Example: router.push({ name: 'dashboard' }) or router.push('/')
      // For now, let's assume a default redirect to a home/dashboard page if it exists
      // or just log success and let router guards handle it.
      // Check if there's a redirect query param
      const redirectPath = router.currentRoute.value.query.redirect || '/';
      router.push(redirectPath);
    } else {
      errorMessage.value = authStore.loginError || 'Login failed. Please check your credentials.';
    }
  } catch (error) {
    // This catch might be redundant if authStore.login handles all errors and sets loginError
    console.error("Login component error:", error);
    errorMessage.value = 'An unexpected error occurred during login.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.login-container h2 {
  text-align: center;
  margin-bottom: 20px;
}
div {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
button:hover {
  background-color: #0056b3;
}
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
.error-message {
  color: red;
  margin-top: 15px;
  text-align: center;
}
</style>
