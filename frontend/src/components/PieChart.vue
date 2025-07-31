<template>
  <div class="chart-container">
    <Doughnut :data="chartData" :options="chartOptions" :width="350" :height="350" />
  </div>
</template>

<script lang="ts" setup>
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  ArcElement
} from 'chart.js'
import type { ChartOptions } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

defineProps<{
  chartData: any
}>()

const chartOptions: ChartOptions<'doughnut'> = {
  responsive: false,            // disable automatic responsiveness
  maintainAspectRatio: false,   // let size be controlled by props/container
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
  width: 350px;
  height: 350px;
  margin: auto;
}
</style>
