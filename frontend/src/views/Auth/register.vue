<template>
  <div class="register-container">
    <header class="app-header">Vehicle Parking</header>
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <div>
        <label>Full Name:</label>
        <input v-model="form.full_name" type="text" required />
      </div>
      <div>
        <label>Email:</label>
        <input v-model="form.email" type="email" required />
      </div>
      <div>
        <label>Address:</label>
        <input v-model="form.address" type="text" required />
      </div>
      <div>
        <label>Pincode:</label>
        <input v-model="form.pincode" type="text" required />
      </div>
      <div>
        <label>Password:</label>
        <input v-model="form.password" type="password" required />
      </div>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from '@/axios';

const router = useRouter();

const form = reactive({
  full_name: '',
  email: '',
  address: '',
  pincode: '',
  password: ''
});

const registerUser = async () => {
  try {
    const res = await axios.post('/register', form);
    alert(res.data.message);
    router.push('/login');
  } catch (err: any) {
    alert(err.response?.data?.error || 'Registration failed');
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1.5rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.register-container h2 {
  text-align: center;
  margin-bottom: 1rem;
}
.register-container form div {
  margin-bottom: 1rem;
}
.register-container input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}

.app-header {
  text-align: center;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #1f2937; /* dark gray */
}

button {
  width: 100%;
  padding: 0.6rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #369f6e;
}
</style>
