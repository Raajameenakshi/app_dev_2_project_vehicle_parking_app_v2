<template>
  <div>
    <AdminHeader />
    <div class="container">
      <h2>All Parking Records</h2>
      <table class="records-table">
        <thead>
          <tr>
            <th>Booking ID</th>
            <th>User</th>
            <th>Lot</th>
            <th>Spot ID</th>
            <th>Vehicle No</th>
            <th>Start</th>
            <th>End</th>
            <th>Cost (₹)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.booking_id">
            <td>{{ record.booking_id }}</td>
            <td>{{ record.user }}</td>
            <td>{{ record.lot }}</td>
            <td>{{ record.spot_id }}</td>
            <td>{{ record.vehicle_number }}</td>
            <td>{{ record.start }}</td>
            <td>{{ record.end }}</td>
            <td>{{ record.cost }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from '@/axios'
import AdminHeader from '@/components/adminheader.vue'

interface BookingRecord {
  booking_id: number
  user: string
  lot: string
  spot_id: number
  vehicle_number: string
  start: string
  end: string
  cost: number
}

const records = ref<BookingRecord[]>([])

onMounted(async () => {
  try {
    const response = await axios.get('/admin/bookings')
    records.value = response.data
  } catch (error) {
    console.error('Failed to fetch bookings:', error)
  }
})
</script>

<style scoped>
.container {
  padding: 2rem;
}

.records-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.records-table th,
.records-table td {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  text-align: left;
}
</style>
