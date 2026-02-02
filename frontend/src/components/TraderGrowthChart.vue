<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { createChart, type ISeriesApi } from 'lightweight-charts'
import { useGrowthStore } from '../stores/growthStore'
import { storeToRefs } from 'pinia'

const chartContainer = ref<HTMLElement | null>(null)
let chart: any = null
let rewardSeries: ISeriesApi<'Line'> | null = null
let sharpeSeries: ISeriesApi<'Line'> | null = null
let mddSeries: ISeriesApi<'Line'> | null = null

const growthStore = useGrowthStore()
const { logs } = storeToRefs(growthStore)

onMounted(async () => {
  await growthStore.fetchLogs()
  growthStore.subscribeToLogs()

  if (chartContainer.value) {
    chart = createChart(chartContainer.value, {
      width: chartContainer.value.clientWidth,
      height: 400,
      layout: {
        background: { color: '#1E1E1E' },
        textColor: '#DDD',
      },
      grid: {
        vertLines: { color: '#2B2B2B' },
        horzLines: { color: '#2B2B2B' },
      },
    })

    rewardSeries = chart.addLineSeries({
      color: '#4caf50',
      title: 'Reward',
      lineWidth: 2,
    })

    mddSeries = chart.addLineSeries({
      color: '#ff5252',
      title: 'MDD',
      lineWidth: 2,
      priceScaleId: 'right',
    })

    sharpeSeries = chart.addLineSeries({
      color: '#2196f3',
      title: 'Sharpe Ratio',
      lineWidth: 2,
      priceScaleId: 'left', // Use left axis for Sharpe
    })
    
    // Check if right axis is visible
    chart.priceScale('right').applyOptions({
         visible: true,
         borderColor: '#2B2B2B'
    });
    
    chart.priceScale('left').applyOptions({
         visible: true,
         borderColor: '#2B2B2B'
    });

    updateChart()
  }
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    if (chart) {
        chart.remove()
    }
})

const handleResize = () => {
    if (chart && chartContainer.value) {
        chart.applyOptions({ width: chartContainer.value.clientWidth })
    }
}

watch(logs, () => {
  updateChart()
}, { deep: true })

function epochToDate(epoch: number): string {
  // Mock date starting from 2024-01-01 plus epoch days
  const date = new Date(2024, 0, 1)
  date.setDate(date.getDate() + epoch)
  return date.toISOString().split('T')[0] || ''
}

function updateChart() {
  if (!chart || !rewardSeries || !sharpeSeries || !mddSeries) return
  if (logs.value.length === 0) return

  // sort logs by epoch
  const sortedLogs = [...logs.value].sort((a, b) => a.epoch - b.epoch)
  
  const rewardData = sortedLogs.map(log => ({ time: epochToDate(log.epoch), value: log.reward }))
  const sharpeData = sortedLogs.map(log => ({ time: epochToDate(log.epoch), value: log.sharpe_ratio }))
  const mddData = sortedLogs.map(log => ({ time: epochToDate(log.epoch), value: log.mdd }))
  
  rewardSeries.setData(rewardData)
  sharpeSeries.setData(sharpeData)
  mddSeries.setData(mddData)
  
  chart.timeScale().fitContent()
}
</script>

<template>
  <div class="chart-wrapper">
    <h2>RL Agent Training Progress</h2>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<style scoped>
.chart-wrapper {
  width: 100%;
  padding: 20px;
  background-color: #121212;
  border-radius: 8px;
}

h2 {
  color: #fff;
  margin-bottom: 10px;
}

.chart-container {
  width: 100%;
  height: 400px;
}
</style>
