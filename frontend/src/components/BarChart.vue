<template>
  <div class="chart-container">
    <Bar :data="chartData" :options="chartOptions" :width="600" :height="400" />
  </div>
</template>

<script lang="ts" setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js'
import type { ChartOptions } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

defineProps<{
  chartData: any
}>()

const chartOptions: ChartOptions<'bar'> = {
  responsive: false,            // disable auto responsiveness
  maintainAspectRatio: false,   // allow fixed size control
  plugins: {
    legend: {
      position: 'top' as const
    },
    title: {
      display: false
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 600px;
  height: 400px;
  margin: auto;
}
</style>
