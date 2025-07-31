<template>
  <div>
    <AdminHeader />
  <div class="container px-4 py-6">
    <h2 class="text-2xl font-bold mb-4">Spot ID: {{ spot?.id }}</h2>
    <div class="mb-4">
      <p>Status:
        <span v-if="spot?.is_booked" class="text-red-600">Occupied</span>
        <span v-else-if="spot?.additional_info === 'Unavailable'" class="text-gray-500">Unavailable</span>
        <span v-else class="text-green-600">Available</span>
      </p>
    </div>

    <div v-if="!spot?.is_booked">
      <button
        v-if="spot?.additional_info !== 'Unavailable'"
        @click="markUnavailable"
        class="btn bg-yellow-500 text-white px-4 py-2 rounded"
      >
        Mark as Unavailable
      </button>

      <button
        v-else
        @click="markAvailable"
        class="btn bg-green-600 text-white px-4 py-2 rounded"
      >
        Mark as Available
      </button>
    </div>

    <div class="mt-6">
      <router-link :to="`/admin/spots/${spotId}/booking`" v-if="spot?.is_booked" class="text-blue-600 underline">
        View Booking Details →
      </router-link>
    </div>

    <router-link :to="`/admin/parking-lots/${spot?.parking_lot_id}`" class="block mt-10 text-gray-600 hover:underline">
      ← Back to Lot
    </router-link>
  </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axios'
import AdminHeader from '@/components/adminheader.vue'

const route = useRoute()
const spotId = Number(route.params.id)
const spot = ref<any>(null)

const fetchSpot = async () => {
  const res = await axios.get(`/admin/spots/${spotId}`)
  spot.value = res.data
}

const markUnavailable = async () => {
  await axios.post(`/admin/spots/${spotId}/unavailable`)
  fetchSpot()
}

const markAvailable = async () => {
  await axios.post(`/admin/spots/${spotId}/available`)
  fetchSpot()
}

onMounted(fetchSpot)
</script>

<style scoped>
.container {
  padding: 2rem 1rem;
  max-width: 800px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

p {
  font-size: 1rem;
  margin: 0.5rem 0;
}

.btn {
  display: inline-block;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s ease;
}

.btn:hover {
  opacity: 0.9;
}

.mt-6 {
  margin-top: 1.5rem;
}

.mt-10 {
  margin-top: 2.5rem;
}

.text-red-600 {
  color: #dc2626;
}

.text-green-600 {
  color: #16a34a;
}

.text-gray-500 {
  color: #6b7280;
}

.text-blue-600 {
  color: #2563eb;
}

.text-blue-600:hover {
  text-decoration: underline;
}

.text-gray-600 {
  color: #4b5563;
}

.text-gray-600:hover {
  text-decoration: underline;
}

.bg-yellow-500 {
  background-color: #eab308;
}

.bg-green-600 {
  background-color: #16a34a;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.rounded {
  border-radius: 0.375rem;
}

.font-bold {
  font-weight: 700;
}

.mb-4 {
  margin-bottom: 1rem;
}
</style>
