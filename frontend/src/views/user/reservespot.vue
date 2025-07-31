<template>
  <div>
    <Header />
    <div class="reserve-container">
      <h2>Reserve Spot</h2>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

      <form @submit.prevent="reserve" class="reserve-form">
        <div class="form-group">
          <label>Lot:</label>
          <input type="text" v-model="lot.location" disabled />
        </div>
        <div class="form-group">
          <label>Spot ID:</label>
          <input type="text" v-model="nextSpotId" disabled />
        </div>
        <div class="form-group">
          <label>Vehicle Number</label>
          <input type="text" v-model="vehicleNumber" required />
        </div>
        <button type="submit">Reserve</button>
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

interface Lot { id: number; location: string }

const route = useRoute()
const router = useRouter()
const lotId = Number(route.params.lotId)
const lot = ref<Lot>({ id: lotId, location: '' })
const nextSpotId = ref<number>(0)
const vehicleNumber = ref('')
const successMessage = ref('') 

onMounted(async () => {
  const { data: l } = await axios.get<Lot>(`/user/lot/${lotId}`)
  lot.value = l
  const { data: next } = await axios.get<{ next_spot: number }>(`/user/lot/${lotId}/next_spot`)
  nextSpotId.value = next.next_spot
})

async function reserve() {
  try {
    await axios.post('/user/reserve', {
      lot_id: lotId,
      vehicle_number: vehicleNumber.value
    })
    successMessage.value = 'Spot reserved successfully!'
    setTimeout(() => router.push({ name: 'Dashboard' }), 1500)
  } catch (error) {
    console.error('Reservation failed:', error)
    successMessage.value = 'Reservation failed. Please try again.'
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