import { createRouter, createWebHistory } from 'vue-router'
import TraderGrowthChart from '../components/TraderGrowthChart.vue'
import TechniquesView from '../views/TechniquesView.vue'
import ModelsView from '../views/ModelsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: TraderGrowthChart
    },
    {
      path: '/techniques',
      name: 'techniques',
      component: TechniquesView
    },
    {
      path: '/models',
      name: 'models',
      component: ModelsView
    }
  ]
})

export default router
