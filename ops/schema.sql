CREATE TABLE IF NOT EXISTS trader_growth_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  epoch INT,
  sharpe_ratio FLOAT,
  mdd FLOAT,
  reward FLOAT
);
