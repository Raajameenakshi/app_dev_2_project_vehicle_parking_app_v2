<template>
  <div>
    <AdminHeader />
    <div class="lot-container">
      <h2>Edit Parking Lot</h2>
      <form @submit.prevent="submitForm" class="lot-form">
        <div class="form-group">
          <label>Location</label>
          <input v-model="lot.location" type="text" required />
        </div>

        <div class="form-group">
          <label>Address</label>
          <textarea v-model="lot.address" required></textarea>
        </div>

        <div class="form-group">
          <label>Pincode</label>
          <input v-model.number="lot.pincode" type="number" required />
        </div>

        <div class="form-group">
          <label>Price</label>
          <input v-model.number="lot.price" type="number" required />
        </div>

        <div class="form-group">
          <label>Max Spots</label>
          <input v-model.number="lot.max_no_spots" type="number" required />
        </div>

        <div class="form-group">
          <label>Landmark</label>
          <input v-model="lot.landmark" type="text" required />
        </div>

        <button type="submit">Update</button>

        <router-link to="/admin/manage-lots" class="inline-block text-sm text-gray-700 hover:underline mt-10">
        ← Back
      </router-link>

      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/axios'
import AdminHeader from '@/components/adminheader.vue'

interface ParkingLot {
  location: string
  address: string
  pincode: number | null
  price: number | null
  max_no_spots: number | null
  landmark: string
}

export default defineComponent({

  components: {
    AdminHeader
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const lotId = route.params.id

    const lot = reactive<ParkingLot>({
      location: '',
      address: '',
      pincode: null,
      price: null,
      max_no_spots: null,
      landmark: ''
    })

    const fetchLot = async () => {
      try {
        const response = await axios.get(`/admin/view-parking-lot/${lotId}`)
        Object.assign(lot, response.data)
      } catch (error) {
        console.error('Error loading lot:', error)
        alert('Could not load parking lot')
        router.push('/admin/manage-lots')
      }
    }

    const submitForm = async () => {
      try {
        await axios.put(`/admin/edit-parking-lot/${lotId}`, lot)
        router.push('/admin/manage-lots')
      } catch (error) {
        console.error('Error updating lot:', error)
        alert('Update failed')
      }
    }

    onMounted(fetchLot)

    return {
      lot,
      submitForm
    }
  }
})
</script>

<style scoped>
.lot-container {
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

.lot-form {
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

input,
textarea {
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
</style>
