<template>
  <div class="navbar">
    <h1 class="title" @click="goToDashboard">Admin Panel</h1>
    <button class="logout-btn" @click="logout">Logout</button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToDashboard = () => {
  router.push('/admin')
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1e1e1e;
  color: white;
  padding: 1rem 2rem;
}

.title {
  font-size: 1.5rem;
  cursor: pointer;
}

.logout-btn {
  background-color: #ff5f5f;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: bold;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
</style>
