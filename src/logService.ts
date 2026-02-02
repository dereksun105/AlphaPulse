import { supabase } from './supabaseClient'
import { TraderGrowthLog } from './types'

export async function uploadTraderGrowthLog(data: TraderGrowthLog) {
  console.log('Uploading log:', data)
  const { error } = await supabase
    .from('trader_growth_log')
    .insert([data])

  if (error) {
    throw new Error(`Error uploading log: ${error.message}`)
  }
  
  console.log('Log uploaded successfully')
}
