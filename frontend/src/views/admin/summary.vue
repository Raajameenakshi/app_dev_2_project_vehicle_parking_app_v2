<template>
  <div>
    <AdminHeader />
    <div class="container">
      <h2>Revenue by Parking Lot</h2>
      <BarChart v-if="revenueChartData" :chart-data="revenueChartData" />

      <h2 class="mt-5">Spot Occupancy per Parking Lot</h2>
      <BarChartStacked v-if="occupancyChartData" :chart-data="occupancyChartData" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from '@/axios'
import AdminHeader from '@/components/adminheader.vue'
import BarChart from '@/components/BarChart.vue'
import BarChartStacked from '@/components/BarChartStacked.vue'

const revenueChartData = ref()
const occupancyChartData = ref()

onMounted(async () => {
  try {
    const response = await axios.get('/admin/summary')
    const { revenue, occupancy } = response.data

    // Prepare revenue chart data
    const revLabels = revenue.map((d: any) => d.location)
    const revValues = revenue.map((d: any) => d.revenue)

    revenueChartData.value = {
      labels: revLabels,
      datasets: [
        {
          label: 'Revenue (₹)',
          backgroundColor: '#4bc0c0',
          data: revValues
        }
      ]
    }

    // Prepare occupancy chart data
    const occLabels = occupancy.map((d: any) => d.location)
    occupancyChartData.value = {
      labels: occLabels,
      datasets: [
        {
          label: 'Available',
          backgroundColor: '#5adbb5',
          data: occupancy.map((d: any) => d.available)
        },
        {
          label: 'Booked',
          backgroundColor: '#f87171',
          data: occupancy.map((d: any) => d.booked)
        },
        {
          label: 'Unavailable',
          backgroundColor: '#a3a3a3',
          data: occupancy.map((d: any) => d.unavailable)
        }
      ]
    }
  } catch (error) {
    console.error('Failed to load analytics dashboard:', error)
  }
})
</script>

<style scoped>
.container {
  padding: 2rem;
}
.mt-5 {
  margin-top: 3rem;
}
</style>
