import { uploadTraderGrowthLog } from './logService'
import { supabase } from './supabaseClient'

async function test() {
  try {
    // 1. Check connection
    console.log('Checking Supabase connection...')
    const { data, error } = await supabase.from('trader_growth_log').select('count', { count: 'exact', head: true })
    
    if (error) {
       // It might fail if table doesn't exist, but that's a useful check
       console.log('Connection check result (might be table missing error):', error.message)
    } else {
       console.log('Connection successful. Row count:', data)
    }

    // 2. Upload data
    const sampleData = {
      epoch: 1,
      sharpe_ratio: 1.5,
      mdd: 0.2,
      reward: 100.5
    }
    await uploadTraderGrowthLog(sampleData)
    
  } catch (err) {
    console.error('Test failed:', err)
  }
}

test()
