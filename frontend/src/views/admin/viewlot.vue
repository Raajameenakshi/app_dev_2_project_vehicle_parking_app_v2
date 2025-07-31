<template>
  <div>
    <AdminHeader />
    <div class="container">
      <br>
      <h2>
        Parking Lot: {{ lot?.location }} (ID: {{ lot?.id }})
      </h2>
      <br>

      <div class="mb-8 space-y-3 text-gray-800 leading-relaxed lot-details">
  <p><strong>Address:</strong> {{ lot?.address }}</p>
  <p><strong>Landmark:</strong> {{ lot?.landmark }}</p>
  <p><strong>Pincode:</strong> {{ lot?.pincode }}</p>
  <p><strong>Price per Unit Time:</strong> ₹{{ lot?.price }}</p>
  <p><strong>Max Spots:</strong> {{ lot?.max_no_spots }}</p>
  <p><strong>Occupancy:</strong> {{ occupiedCount }} / {{ lot?.max_no_spots }} spots occupied</p>
</div>


      <hr class="my-8 border-gray-300" />

      <h4 class="text-xl font-medium mb-6 text-gray-900">Parking Spots</h4>

      <div class="spot-container">
  <router-link
    v-for="(spot, index) in spots"
    :key="spot.id"
    :to="`/admin/spots/${spot.id}`"
    class="spot-box"
    :class="{
      'available': !spot.is_booked && spot.additional_info !== 'Unavailable',
      'booked': spot.is_booked,
      'unavailable': spot.additional_info === 'Unavailable'
    }"
  >
    <div class="text-center">
      <h4 class="font-semibold">Spot {{ index + 1 }}</h4>
      <p class="text-sm">
        {{ spot.is_booked ? 'Occupied' : (spot.additional_info === 'Unavailable' ? 'Unavailable' : 'Available') }}
      </p>
    </div>
  </router-link>
</div>
<br>
      <router-link to="/admin/manage-lots" class="inline-block text-sm text-gray-700 hover:underline mt-10">
        ← Back to All Lots
      </router-link>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axios'
import AdminHeader from '@/components/adminheader.vue'

interface ParkingLot {
  id: number
  location: string
  address: string
  landmark: string
  pincode: string
  price: number
  max_no_spots: number
}

interface ParkingSpot {
  id: number
  is_booked: boolean
  additional_info: string
}

const route = useRoute()
const lotId = Number(route.params.id)

const lot = ref<ParkingLot | null>(null)
const spots = ref<ParkingSpot[]>([])

const fetchLotData = async () => {
  try {
    const res = await axios.get(`/admin/view-parking-lot/${lotId}`)
    lot.value = res.data.lot
    spots.value = res.data.spots
  } catch (err) {
    console.error('Failed to fetch lot data:', err)
  }
}

const occupiedCount = computed(() =>
  spots.value.filter((s) => s.is_booked).length
)


onMounted(() => {
  fetchLotData()
})
</script>

<style scoped>
.spot-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: flex-start;
}

.spot-box {
  width: 150px;
  height: 100px;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  color: white;
  text-decoration: none;
  transition: transform 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.spot-box:hover {
  transform: scale(1.05);
}

.available {
  background-color: #38a169; /* green */
}

.booked {
  background-color: #e53e3e; /* red */
}

.unavailable {
  background-color: #d69e2e; /* yellow */
}

/* Text block spacing */
.lot-details > p {
  margin-bottom: 0.5rem;
}

/* Divider spacing */
hr {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

</style>
