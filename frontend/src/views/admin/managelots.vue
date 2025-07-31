<template>
  <div>
    <AdminHeader />
    <div class="container">
      <h2>Parking Lots</h2>
      <router-link to="/admin/parking-lots/create" class="add-lot-link">Add New Lot</router-link>
      
      <table v-if="lots.length" class="lot-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Location</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lot in lots" :key="lot.id">
            <td>{{ lot.id }}</td>
            <td>{{ lot.location }}</td>
            <td>{{ lot.address }}</td>
            <td>{{ lot.pincode }}</td>
            <td>
              <router-link :to="`/admin/parking-lots/${lot.id}`" class="action-link view">View</router-link>
              <router-link :to="`/admin/parking-lots/${lot.id}/edit`" class="action-link edit">Edit</router-link>
              <button class="action-link delete" @click="deleteLot(lot.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-else>No parking lots found.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axios'
import AdminHeader from '@/components/adminheader.vue'

interface ParkingLot {
  id: number
  location: string
  address: string
  pincode: number
  price: number
  max_no_spots: number
  landmark: string
}

export default {
  components: { AdminHeader },
  setup() {
    const router = useRouter()
    const lots = ref<ParkingLot[]>([])

    const fetchLots = async () => {
      try {
        const response = await axios.get('/admin/parking-lots')
        lots.value = response.data
      } catch (error) {
        console.error('Failed to fetch parking lots', error)
      }
    }

    const deleteLot = async (id: number) => {
      const confirmDelete = confirm('Are you sure you want to delete this lot?')
      if (!confirmDelete) return

      try {
        await axios.delete(`/admin/del-parking-lot/${id}`)
        fetchLots()
      } catch (error) {
        console.error('Failed to delete parking lot', error)
        alert('Delete failed')
      }
    }

    onMounted(() => {
      fetchLots()
    })

    return {
      lots,
      deleteLot
    }
  }
}
</script>


<style scoped>
.container {
  padding: 2rem;
}

.add-lot-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #00a86b;
  font-weight: 500;
}

.lot-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.lot-table th,
.lot-table td {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  text-align: left;
}

.action-link {
  margin-right: 0.5rem;
  text-decoration: none;
  padding: 0.4rem 0.7rem;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
}

.view {
  background-color: #2d9cdb;
  color: white;
}

.edit {
  background-color: #f2c94c;
  color: black;
}

.delete {
  background-color: #eb5757;
  color: white;
  border: none;
}
</style>
