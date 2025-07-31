<template>
  <div>
    <Header />
    <div class="reserve-container">
      <h2>Release Spot</h2>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <form @submit.prevent="release" class="reserve-form">
        <div class="form-group">
          <label>Spot ID:</label>
          <input v-model="booking.spot_id" disabled />
        </div>
        <div class="form-group">
          <label>Vehicle:</label>
          <input v-model="booking.vehicle_number" disabled />
        </div>
        <div class="form-group">
          <label>Start Time:</label>
          <input :value="formattedStartTime" disabled />
        </div>
        <div class="form-group">
          <label>Estimated End Time:</label>
          <input :value="estimatedEndTime" disabled />
        </div>
        <div class="form-group">
          <label>Rate (per hour):</label>
          <input :value="lotPrice !== null ? '₹' + lotPrice + '/hr' : 'Loading...'" disabled />
        </div>
        <button type="submit">Release</button>
        <router-link to="/user" class="inline-block text-sm text-gray-700 hover:underline mt-10">
        ← Back
      </router-link>
      </form>
    </div>
  </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/axios'
import Header from '@/components/userheader.vue'

import { computed } from 'vue'

const estimatedEndTime = computed(() => {
  if (!booking.value) return ''
  if (booking.value.is_active) {
    return new Date().toLocaleString('en-IN', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  hour12: true
}) // Current time as estimated end time
  }
  return booking.value.end_time
})

const formattedStartTime = computed(() => {
  if (!booking.value.start_time) return ''
  return new Date(booking.value.start_time).toLocaleString('en-IN', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  hour12: true
})
})

const successMessage = ref('') 

interface Booking { id: number; spot_id: number; vehicle_number: string; start_time: string; end_time: string; cost: number; is_active: boolean }

const route = useRoute()
const router = useRouter()
const bookingId = Number(route.params.bookingId)
const booking = ref<Booking>({
  id: bookingId, spot_id: 0, vehicle_number: '', start_time: '', end_time: '', cost: 0, is_active: true
})
const lotPrice = ref<number | null>(null)

onMounted(async () => {
  const { data } = await axios.get<Booking>(`/user/booking/${bookingId}`)
  booking.value = data
  // Get spot details to find parking_lot_id
  const spotRes = await axios.get(`/user/spot/${data.spot_id}`)
  const lotId = spotRes.data.parking_lot_id

  // Get lot details to get the price
  const lotRes = await axios.get(`/user/lot/${lotId}`)
  lotPrice.value = lotRes.data.price
})

async function release() {
    try {
        await axios.post(`/user/booking/${bookingId}/release`)
        successMessage.value = 'Spot released successfully!'
        setTimeout(() => router.push({ name: 'Dashboard' }), 1500)
    } catch (error) {
        console.error('Release failed:', error)
        successMessage.value = 'Error in Releasing!'
    }
}
</script>

<style scoped>
.reserve-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
}

h2 {
  text-align: center;
  margin-bottom: 1rem;
}

.reserve-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  padding: 0.75rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #059669;
}

.success-message {
  background-color: #d1fae5;
  color: #065f46;
  border: 1px solid #10b981;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 500;
}
</style>
