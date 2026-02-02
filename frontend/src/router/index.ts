import { createRouter, createWebHistory } from 'vue-router'
import TraderGrowthChart from '../components/TraderGrowthChart.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: TraderGrowthChart
    }
  ]
})

export default router
