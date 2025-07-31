<template>
  <div>
    <AdminHeader />
    <div class="container">
      <h2>Registered Users</h2>
      <table class="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Full Name</th>
            <th>Address</th>
            <th>Pincode</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.full_name }}</td>
            <td>{{ user.address }}</td>
            <td>{{ user.pincode }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import axios from '@/axios'
import AdminHeader from '@/components/adminheader.vue'

interface User {
  id: number
  email: string
  full_name: string
  address: string
  pincode: number
}

const users = ref<User[]>([])

onMounted(async () => {
  try {
    const response = await axios.get('/admin/users')
    users.value = response.data
  } catch (error) {
    console.error('Failed to fetch users', error)
  }
})
</script>

<style scoped>
.container {
  padding: 2rem;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.user-table th,
.user-table td {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  text-align: left;
}
</style>
