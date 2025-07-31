<template>
  <div class="dashboard">
    <Header />
    <div class="container">
      <section>
        <h2>Available Parking Lots</h2>
        <table>
          <thead>
            <tr>
              <th>Lot</th>
              <th>Address</th>
              <th>Price</th>
              <th>Spots Free</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in lots" :key="lot.id">
              <td>{{ lot.location }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.price }}</td>
              <td>{{ lot.spots_free }}</td>
              <td>
                <router-link v-if="lot.spots_free > 0"
                             :to="{ name: 'ReserveSpot', params: { lotId: lot.id }}">
                  <button>Book</button>
                </router-link>
                <span v-else>Full</span>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section>
        <h2>Parking History</h2>
        <table>
          <thead>
            <tr>
              <th>Spot ID</th>
              <th>Vehicle</th>
              <th>Start</th>
              <th>End</th>
              <th>Duration</th>
              <th>Cost</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in bookings" :key="b.id">
              <td>{{ b.spot_id }}</td>
              <td>{{ b.vehicle_number }}</td>
              <td>{{ formatTime(b.start_time) }}</td>
              <td>
                <span v-if="!b.is_active">{{ formatTime(b.end_time) }}</span>
                <span v-else>Active</span>
              </td>
              <td>
                <span v-if="!b.is_active">{{ computeDuration(b.start_time, b.end_time) }}</span>
                <span v-else>--</span>
              </td>
              <td>
                <span v-if="!b.is_active">₹{{ b.cost }}</span>
                <span v-else>--</span>
              </td>
              <td>
                <router-link v-if="b.is_active"
                             :to="{ name: 'ReleaseSpot', params: { bookingId: b.id }}">
                  <button>Release</button>
                </router-link>
                <button disabled v-else>Released</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="summary-button-container">
          <router-link :to="{ name: 'UserSummary' }">
          <button>View Summary</button>
            </router-link>
            <button @click="exportCsv" :disabled="isExporting">
            {{ isExporting ? 'Generating CSV...' : 'Export My Parking History' }}
          </button>
        </div>

        <div v-if="csvDownloadUrl" class="csv-download-link">
          ✅ Your report is ready.
          <a :href="csvDownloadUrl" download target="_blank">Download CSV</a>
        </div>

      </section>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from '@/axios'
import Header from '@/components/userheader.vue'

interface Lot {
  id: number
  location: string
  address: string
  price: number
  spots_free: number
}

interface Booking {
  id: number
  spot_id: number
  vehicle_number: string
  start_time: string
  end_time: string | null
  cost: number
  is_active: boolean
}

const lots = ref<Lot[]>([])
const bookings = ref<Booking[]>([])
const isExporting = ref(false)
const csvDownloadUrl = ref<string | null>(null)

function formatTime(datetime: string | null): string {
  if (!datetime) return '--'
  const date = new Date(datetime)
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function computeDuration(start: string, end: string | null): string {
  if (!end) return '--'

  const startDate = new Date(start)
  const endDate = new Date(end)
  let diffMs = endDate.getTime() - startDate.getTime()

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


async function loadData() {
  const [lotRes, bookRes] = await Promise.all([
    axios.get('/user/available_lots'),
    axios.get('/user/bookings')
  ])
  lots.value = lotRes.data
  bookings.value = bookRes.data
}

async function exportCsv() {
  isExporting.value = true
  csvDownloadUrl.value = null

  try {
    const { data } = await axios.post('/export-csv')
    const taskId = data.task_id

    const poll = async (attempt = 0) => {
      if (attempt >= 10) {
        alert("CSV generation timed out.")
        isExporting.value = false
        return
      }

      try {
        const response = await axios.get(`/csv_result/${taskId}`, {
          responseType: 'blob'
        })

        const contentDisposition = response.headers['content-disposition']
        if (contentDisposition && response.data) {
          const blobUrl = URL.createObjectURL(response.data)
          csvDownloadUrl.value = blobUrl
          isExporting.value = false
        } else {
          setTimeout(() => poll(attempt + 1), 2000)
        }
      } catch (error: any) {
        if (error.response?.status === 202) {
          setTimeout(() => poll(attempt + 1), 2000)
        } else {
          console.error("CSV download error:", error)
          alert("Failed to download CSV.")
          isExporting.value = false
        }
      }
    }

    poll()
  } catch (err) {
    console.error("Export failed:", err)
    alert("Could not start export.")
    isExporting.value = false
  }
}

onMounted(loadData)

</script>


<style scoped>
.container {
  padding: 2rem;
  max-width: 900px;
  margin: auto;
  font-family: Arial, sans-serif;
  color: #333;
}

h2 {
  margin-bottom: 1rem;
  font-weight: 600;
  font-size: 1.5rem;
  border-bottom: 2px solid #ddd;
  padding-bottom: 0.25rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
  overflow: hidden;
}

thead tr {
  background-color: #f4f6f8;
  font-weight: 600;
  color: black;
  border-bottom: 2px solid #ddd;
}

th, td {
  padding: 0.75rem 1rem;
  text-align: left;
  color:black;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

tbody tr:hover {
  background-color: #fafafa;
}

button {
  background-color: #2a9d8f;
  border: none;
  color: white;
  padding: 0.4rem 0.9rem;
  font-size: 0.9rem;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: #21867a;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  color: #666;
}

.csv-download-link {
  margin-top: 1rem;
  color: #2a9d8f;
  font-weight: 500;
}

.csv-download-link a {
  color: #1e88e5;
  text-decoration: underline;
  margin-left: 0.5rem;
}

</style>

