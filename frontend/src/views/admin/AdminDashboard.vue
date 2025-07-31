<template>
  <div class="admin-container">
    <!-- Top Admin Header -->
    <AdminHeader />

    <!-- Buttons area -->
    <div class="button-group">
      <button class="nav-btn" @click="goToManageUsers">Manage Users</button>
      <button class="nav-btn" @click="goToManageLots">Manage Lots</button>
      <button class="nav-btn" @click="goToBookings">View Bookings</button>
      <button class="nav-btn" @click="goToSummary">Summary</button>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import AdminHeader from '@/components/adminheader.vue' // adjust path if needed

const router = useRouter()

const goToManageLots = () => {
  router.push('/admin/manage-lots')
}

const goToManageUsers = () => {
  router.push('/admin/view-users')
}

const goToBookings = () => {
  router.push('/admin/bookings')
}

const goToSummary = () => {
  router.push('/admin/summary')
}
</script>

<style scoped>
.admin-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Segoe UI', sans-serif;
  background-color: white;
  width: 100%;
}

/* Buttons */
.button-group {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 3rem;
  flex-wrap: wrap;
}

.nav-btn {
  padding: 1.5rem 2rem;
  font-size: 1.2rem;
  border: none;
  background-color: #2f80ed;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  min-width: 200px;
  transition: background-color 0.3s ease;
}

.nav-btn:hover {
  background-color: #1366d6;
}
</style>
