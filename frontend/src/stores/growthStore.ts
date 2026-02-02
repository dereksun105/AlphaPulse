import { defineStore } from 'pinia'
import { supabase } from '../supabase'
import type { TraderGrowthLog } from '../types'
import { TRADER_GROWTH_LOG_TABLE } from '../types'

export const useGrowthStore = defineStore('growth', {
  state: () => ({
    logs: [] as TraderGrowthLog[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchLogs() {
      this.loading = true
      this.error = null
      try {
        const { data, error } = await supabase
          .from(TRADER_GROWTH_LOG_TABLE)
          .select('*')
          .order('epoch', { ascending: true })

        if (error) throw error
        this.logs = data as TraderGrowthLog[]
      } catch (err: any) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    subscribeToLogs() {
      supabase
        .channel('public:trader_growth_log')
        .on(
          'postgres_changes',
          { event: 'INSERT', schema: 'public', table: TRADER_GROWTH_LOG_TABLE },
          (payload) => {
            console.log('New log received!', payload)
            this.logs.push(payload.new as TraderGrowthLog)
            // Sort again just in case, or apppend correctly
            this.logs.sort((a, b) => a.epoch - b.epoch)
          }
        )
        .subscribe()
    }
  }
})
