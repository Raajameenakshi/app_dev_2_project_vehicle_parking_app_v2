<template>
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
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axios'

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
