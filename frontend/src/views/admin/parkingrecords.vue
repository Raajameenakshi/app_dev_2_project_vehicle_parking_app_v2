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
            <th>Duration</th>
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
            <td>{{ computeDuration(record.start, record.end) }}</td>
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

function computeDuration(start: string, end: string | null): string {
  if (!end) return '--'

  function parseDate(dateStr: string): Date {
    // Expects: DD-MM-YYYY HH:mm
    const [datePart, timePart] = dateStr.split(' ')
    const [day, month, year] = datePart.split('-').map(Number)
    const [hour, minute] = timePart.split(':').map(Number)
    return new Date(year, month - 1, day, hour, minute)
  }

  const startDate = parseDate(start)
  const endDate = parseDate(end)
  const diffMs = endDate.getTime() - startDate.getTime()

  if (diffMs <= 0) return '0s'

  const seconds = Math.floor((diffMs / 1000) % 60)
  const minutes = Math.floor((diffMs / (1000 * 60)) % 60)
  const hours = Math.floor((diffMs / (1000 * 60 * 60)) % 24)
  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  const parts = []
  if (days > 0) parts.push(`${days}d`)
  if (hours > 0) parts.push(`${hours}h`)
  if (minutes > 0) parts.push(`${minutes}m`)
  if (seconds > 0 || parts.length === 0) parts.push(`${seconds}s`)

  return parts.join(' ')
}


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
