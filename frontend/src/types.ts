export const TRADER_GROWTH_LOG_TABLE = 'trader_growth_log'

export interface TraderGrowthLog {
  id: string
  created_at: string
  epoch: number
  sharpe_ratio: number
  mdd: number
  reward: number
}
