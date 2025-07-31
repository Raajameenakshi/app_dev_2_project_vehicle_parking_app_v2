<template>
  <div>
    <UserHeader />
    <div class="container">
      <h2>Your Parking Summary</h2>
      <div class="summary-card">
        <strong>Total Spent: ₹{{ totalSpent }}</strong>
      </div>

      <h3 class="mt-4">Monthly Cost (₹)</h3>
      <BarChart v-if="monthlyChartData" :chart-data="monthlyChartData" />

      <h3 class="mt-5">Cost by Parking Lot</h3>
      <DoughnutChart v-if="lotChartData" :chart-data="lotChartData" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from '@/axios'
import UserHeader from '@/components/userheader.vue'
import BarChart from '@/components/BarChart.vue'
import DoughnutChart from '@/components/PieChart.vue'

const totalSpent = ref(0)
const monthlyChartData = ref()
const lotChartData = ref()

onMounted(async () => {
  try {
    const res = await axios.get('/user/summary')
    const data = res.data

    totalSpent.value = data.total

    // Monthly bar chart
    monthlyChartData.value = {
      labels: data.monthly.map((m: any) => monthLabel(m.month)),
      datasets: [{
        label: '₹ Spent',
        backgroundColor: '#4bc0c0',
        data: data.monthly.map((m: any) => m.cost)
      }]
    }

    // Doughnut chart for cost by lot
    lotChartData.value = {
      labels: data.by_lot.map((l: any) => l.location),
      datasets: [{
        backgroundColor: ['#f87171', '#fbbf24', '#34d399', '#60a5fa', '#a78bfa'],
        data: data.by_lot.map((l: any) => l.cost)
      }]
    }
  } catch (err) {
    console.error('Error fetching user summary:', err)
  }
})

function monthLabel(monthNum: number): string {
  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                      'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return monthNames[monthNum - 1] ?? `Month ${monthNum}`
}
</script>

<style scoped>
.container {
  padding: 2rem;
}

.summary-card {
  background-color: #d1fae5;
  padding: 1rem;
  margin-bottom: 2rem;
  border-radius: 0.5rem;
  font-size: 1.2rem;
}

.mt-4 {
  margin-top: 2rem;
}

.mt-5 {
  margin-top: 3rem;
}
</style>
