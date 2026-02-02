<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { createChart, type ISeriesApi, type IChartApi, AreaSeries } from 'lightweight-charts';
import { supabase } from '../supabase';

// CRITICAL: Use plain variables for Chart instances, NOT Vue refs.
// Vue proxies interfere with Lightweight Charts internal logic.
// This follows the Official TradingView Vue.js Best Practices guide.
let chart: IChartApi | null = null;
let lineSeries: ISeriesApi<"Area"> | null = null;

const chartContainer = ref<HTMLElement | null>(null);
const latestStats = ref<any>(null);

// Helper to convert epoch to a strict YYYY-MM-DD string
function epochToDateString(epoch: number): string {
  const date = new Date(2024, 0, 1);
  date.setDate(date.getDate() + Number(epoch));
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
}

const resizeHandler = () => {
    if (!chart || !chartContainer.value) return;
    const { clientWidth } = chartContainer.value;
    // Make chart responsive to window height (75% of viewport)
    chart.applyOptions({ width: clientWidth, height: window.innerHeight * 0.75 });
};

onMounted(async () => {
  if (!chartContainer.value) return;

  // 1. Initialize Chart
  chart = createChart(chartContainer.value, {
    height: window.innerHeight * 0.75, 
    width: chartContainer.value.clientWidth,
    layout: { 
        background: { color: '#1a1a1a' }, 
        textColor: '#d1d4dc',
    },
    grid: { 
        vertLines: { color: '#2b2b2b' }, 
        horzLines: { color: '#2b2b2b' } 
    },
    timeScale: {
      borderColor: '#2b2b2b',
      timeVisible: true,
    },
    rightPriceScale: {
      borderColor: '#2b2b2b',
    },
  });

  // 2. Add Series
  lineSeries = chart.addSeries(AreaSeries, {
    lineColor: '#2962FF', 
    topColor: '#2962FF', 
    bottomColor: 'rgba(41, 98, 255, 0.28)',
    lineWidth: 2,
  });

  // 3. Fetch Initial Data
  const { data } = await supabase
    .from('trader_growth_log')
    .select('*')
    .order('epoch', { ascending: true });

  if (data && data.length > 0) {
    // Deduplicate and Sort
    const uniqueMap = new Map();
    data.forEach(d => uniqueMap.set(d.epoch, d));
    const sortedData = Array.from(uniqueMap.values()).sort((a: any, b: any) => a.epoch - b.epoch);

    const chartData = sortedData.map((d: any) => ({ 
      time: epochToDateString(d.epoch), 
      value: Number(d.reward) 
    }));

    lineSeries.setData(chartData);
    latestStats.value = sortedData[sortedData.length - 1];
    
    chart.timeScale().fitContent();
  }

  // 4. Realtime Subscription
  supabase
    .channel('growth-realtime')
    .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'trader_growth_log' }, payload => {
      const newLog = payload.new;
      if (newLog && lineSeries) {
        lineSeries.update({ 
          time: epochToDateString(newLog.epoch), 
          value: Number(newLog.reward) 
        });
        latestStats.value = newLog;
      }
    })
    .subscribe();
    
    window.addEventListener('resize', resizeHandler);
});

onUnmounted(() => {
  if (chart) {
    chart.remove();
    chart = null;
  }
  window.removeEventListener('resize', resizeHandler);
});
</script>

<template>
  <div class="growth-dashboard">
    <h3>策略成長監控 (2026 準備計畫)</h3>
    <div ref="chartContainer" class="tv-chart"></div>
    <div class="metrics" v-if="latestStats">
      <span>當前 Sharpe: <span class="highlight">{{ Number(latestStats.sharpe_ratio).toFixed(2) }}</span></span>
      <span>當前 MDD: <span class="down">{{ (Number(latestStats.mdd) * 100).toFixed(2) }}%</span></span>
      <span>回報: <span class="highlight">{{ Number(latestStats.reward).toFixed(2) }}</span></span>
    </div>
    <div class="metrics" v-else>
      <span>等待數據中... (請執行 python/test_rl_upload.py)</span>
    </div>
  </div>
</template>

<style scoped>
.growth-dashboard { 
  background: #111; 
  padding: 20px; 
  border-radius: 8px; 
  border: 1px solid #333;
  box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  font-family: 'Inter', sans-serif;
}
.growth-dashboard h3 {
  color: #fff;
  margin-top: 0;
  margin-bottom: 20px;
  font-weight: 600;
  font-size: 1.1rem;
  border-left: 4px solid #2962FF;
  padding-left: 10px;
}
.tv-chart { 
  width: 100%; 
  height: 75vh;
}
.metrics { 
  display: flex; 
  gap: 20px; 
  margin-top: 15px; 
  color: #888; 
  font-family: 'SF Mono', 'Roboto Mono', monospace; 
  font-size: 0.9rem;
  padding-top: 15px;
  border-top: 1px solid #2b2b2b;
}
.highlight { color: #2962FF; font-weight: bold; }
.down { color: #FF5252; font-weight: bold; }
</style>
