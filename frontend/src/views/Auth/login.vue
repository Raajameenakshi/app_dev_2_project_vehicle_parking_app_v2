<template>
  <div class="login-container">
    <header class="app-header">Vehicle Parking</header>

    <h2>Login</h2>
    <form @submit.prevent="loginUser" class="login-form">
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          required
        />
      </div>

      <button type="submit">Login</button>
      <p class="register-link">
        Don’t have an account?
        <a href="#" @click.prevent="goToRegister">Register here</a>
      </p>
    </form>
  </div>
</template>


<script lang="ts" setup>
import { reactive } from 'vue';
import axios from '@/axios';
import { useRouter } from 'vue-router';

const router = useRouter();

interface LoginForm {
  email: string;
  password: string;
}

const form = reactive<LoginForm>({
  email: '',
  password: ''
});

const loginUser = async () => {
  try {
    const res = await axios.post('/login', form);
    localStorage.setItem('token', res.data.access_token);
    localStorage.setItem('role', res.data.role);

    if (res.data.role === 'admin') {
      await router.push('/admin');
    } else {
      await router.push('/user');
    }
  } catch (err: any) {
    alert(err.response?.data?.message || 'Login failed');
  }
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}

h2 {
  text-align: center;
}

.app-header {
  text-align: center;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #1f2937; /* dark gray */
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

button {
  padding: 0.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #2563eb;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
}

.register-link a {
  color: #3b82f6;
  text-decoration: none;
}
</style>

