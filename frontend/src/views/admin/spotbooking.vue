<template>
  <div>
    <AdminHeader />
    <div class="container mt-5">
      <h2 class="text-2xl font-bold mb-4">
        Booking Details for Spot {{ booking?.parking_spot.id }}
      </h2>

      <table class="booking-table">
        <tbody v-if="booking && user">
          <tr>
            <th>Booking ID</th>
            <td>{{ booking.id }}</td>
          </tr>
          <tr>
            <th>User ID and Username</th>
            <td>{{ booking.user_id }} - {{ user.full_name }}</td>
          </tr>
          <tr>
            <th>Spot ID</th>
            <td>{{ booking.parking_spot.id }}</td>
          </tr>
          <tr>
            <th>Parking Lot ID</th>
            <td>{{ booking.parking_spot.parking_lot_id }}</td>
          </tr>
          <tr>
            <th>Vehicle Number</th>
            <td>{{ booking.vehicle_number }}</td>
          </tr>
          <tr>
            <th>Start Time</th>
            <td>{{ formatTime(booking.start_time) }}</td>
          </tr>
          <tr>
            <th>End Time</th>
            <td>{{ '—' }}</td>
          </tr>
          <tr>
            <th>Cost</th>
            <td>{{ booking.cost ? `₹${booking.cost}` : 'To be calculated' }}</td>
          </tr>
        </tbody>
      </table>

      <router-link
        :to="`/admin/spots/${spotId}`"
        class="back-button"
      >
        ← Back to Spot
      </router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import axios from '@/axios'
import { useRoute } from 'vue-router'
import AdminHeader from '@/components/adminheader.vue' // Make sure path is correct

interface Booking {
  id: number
  user_id: number
  parking_spot_id: number
  vehicle_number: string
  start_time: string
  end_time: string
  cost: number
  parking_spot: {
    id: number
    parking_lot_id: number
  }
}

interface User {
  full_name: string
  email: string
}

export default defineComponent({
  name: 'BookingDetails',
  components: {
    AdminHeader
  },
  setup() {
    const route = useRoute()
    const spotId = route.params.id as string

    const booking = ref<Booking | null>(null)
    const user = ref<User | null>(null)

    const fetchData = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get(`/admin/spots/${spotId}/booking`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        booking.value = response.data.booking
        user.value = response.data.user
      } catch (error) {
        console.error('Error fetching booking details:', error)
      }
    }

    const formatTime = (datetime: string): string => {
      const date = new Date(datetime)
      return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(fetchData)

    return {
      spotId,
      booking,
      user,
      formatTime
    }
  }
})
</script>

<style scoped>
.container {
  max-width: 800px;
  padding: 2rem;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.booking-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

.booking-table th,
.booking-table td {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  text-align: left;
  vertical-align: top;
}

.booking-table th {
  background-color: #f1f1f1;
  font-weight: 600;
}

.back-button {
  display: inline-block;
  background-color: #6b7280; /* gray-500 */
  color: white;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  text-decoration: none;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #4b5563; /* gray-600 */
}
</style>
