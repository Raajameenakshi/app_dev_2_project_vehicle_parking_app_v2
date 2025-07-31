<template>
  <div class="container mt-5">
    <h2 class="text-2xl font-bold mb-4">Booking Details for Spot {{ booking?.parking_spot.id }}</h2>

    <table class="table-auto w-full border border-gray-300 mb-6 text-sm md:text-base">
      <tbody v-if="booking && user">
        <tr>
          <th class="border px-4 py-2 text-left">Booking ID</th>
          <td class="border px-4 py-2">{{ booking.id }}</td>
        </tr>
        <tr>
          <th class="border px-4 py-2 text-left">User ID and Username</th>
          <td class="border px-4 py-2">{{ booking.user_id }} - {{ user.full_name }}</td>
        </tr>
        <tr>
          <th class="border px-4 py-2 text-left">Spot ID</th>
          <td class="border px-4 py-2">{{ booking.parking_spot.id }}</td>
        </tr>
        <tr>
          <th class="border px-4 py-2 text-left">Parking Lot ID</th>
          <td class="border px-4 py-2">{{ booking.parking_spot.parking_lot_id }}</td>
        </tr>
        <tr>
          <th class="border px-4 py-2 text-left">Vehicle Number</th>
          <td class="border px-4 py-2">{{ booking.vehicle_number }}</td>
        </tr>
        <tr>
          <th class="border px-4 py-2 text-left">Start Time</th>
          <td class="border px-4 py-2">{{ formatTime(booking.start_time) }}</td>
        </tr>
        <tr>
          <th class="border px-4 py-2 text-left">End Time</th>
          <td class="border px-4 py-2">{{ formatTime(booking.end_time) }}</td>
        </tr>
        <tr>
          <th class="border px-4 py-2 text-left">Cost</th>
          <td class="border px-4 py-2">₹{{ booking.cost }}</td>
        </tr>
      </tbody>
    </table>

    <router-link
      :to="`/admin/spots/${spotId}`"
      class="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded"
    >
      Back to Spot
    </router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import axios from '@/axios'
import { useRoute } from 'vue-router'

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
  max-width: 700px;
}
</style>
