CREATE TABLE IF NOT EXISTS trader_growth_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  epoch INT,
  sharpe_ratio FLOAT,
  mdd FLOAT,
  reward FLOAT
);

-- 新增：市場盤口數據紀錄 (模擬 CME/CBOE 數據結構)
CREATE TABLE IF NOT EXISTS market_depth_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  symbol TEXT NOT NULL,
  bid_price FLOAT,
  ask_price FLOAT,
  spread FLOAT,
  meta_data JSONB -- 用於儲存更多 Order Book 細節 (如前 5 檔深度)
);
