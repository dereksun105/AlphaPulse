import gymnasium as gym
import numpy as np
import pandas as pd
from gymnasium import spaces

class TradingEnv(gym.Env):
    """
    A custom Trading Environment that follows the user's Risk-Adjusted Reward logic.
    """
    def __init__(self, df: pd.DataFrame, initial_balance=100000.0):
        super(TradingEnv, self).__init__()
        
        self.df = df
        self.initial_balance = initial_balance
        self.current_step = 0
        
        # State: Open, High, Low, Close, Volume
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(5,), dtype=np.float32
        )
        
        # Actions: 0=Hold, 1=Buy, 2=Sell, 3=Close All
        self.action_space = spaces.Discrete(4)
        
        # Internal State logic
        self.balance = initial_balance
        self.positions = 0
        self.entry_price = 0.0
        self.peak_equity = initial_balance
        self.current_equity = initial_balance
        
        self.recent_returns = [] # Store recent returns for volatility calculation
        self.returns_window = 20 # Window size for volatility

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.balance = self.initial_balance
        self.positions = 0
        self.entry_price = 0.0
        self.peak_equity = self.initial_balance
        self.current_equity = self.initial_balance
        self.recent_returns = []
        
        return self._next_observation(), {}

    def _next_observation(self):
        # Mock observation based on current step
        # In real scenario: self.df.iloc[self.current_step]
        row = self.df.iloc[self.current_step]
        return np.array([row['open'], row['high'], row['low'], row['close'], row['volume']], dtype=np.float32)

    def step(self, action):
        current_price = self.df.iloc[self.current_step]['close']
        
        # Execute Action Logic (Simplified for brevity)
        # ... (Buy/Sell logic updating self.positions and self.balance)
        
        # Update Equity
        position_val = self.positions * current_price
        self.current_equity = self.balance + position_val
        self.peak_equity = max(self.peak_equity, self.current_equity)
        
        # Determine Position Type (1=Long, -1=Short, 0=None for simplified context)
        position_type = 1 if self.positions > 0 else (-1 if self.positions < 0 else 0)
        
        # --- USER'S REWARD LOGIC IS HERE ---
        reward = self._get_reward(action, current_price, self.entry_price, position_type)
        # -----------------------------------
        
        # Track returns (pnl percentage mostly) to update recent_returns list
        # For simplicity, just using reward as a proxy for 'return' magnitude here, 
        # but ideally this should be pct_change of equity.
        daily_ret = (self.current_equity - (self.current_equity - reward)) / (self.current_equity - reward + 1e-9) 
        self.recent_returns.append(daily_ret)
        if len(self.recent_returns) > self.returns_window:
            self.recent_returns.pop(0)

        self.current_step += 1
        terminated = self.current_step >= len(self.df) - 1
        truncated = False
        
        return self._next_observation(), reward, terminated, truncated, {}

    def _calculate_pnl(self, current_price, entry_price, position_type):
        """
        Calculates unrealized PnL based on position
        """
        if position_type == 0:
            return 0
        
        # Simple size=1 assumption for calculation demo
        size = abs(self.positions)
        if position_type == 1: # Long
            return (current_price - entry_price) * size
        elif position_type == -1: # Short
            return (entry_price - current_price) * size
        return 0

    def _get_reward(self, action, current_price, entry_price, position_type):
        """
        這段邏輯展現了 Derek 對於「期望值」與「風險控管」的洞察力
        """
        # 1. 計算基礎盈虧 (Realized PnL)
        # Note: In RL step, we usually use change in equity (Unrealized PnL change) as reward for dense signals
        # But following the user prompt strict structure:
        pnl = self._calculate_pnl(current_price, entry_price, position_type)
        
        # 2. 扣除摩擦成本 (交易員的紀律)
        # 優式強調「執行紀律」，這包含對手續費與滑價的敏感度
        trading_fee = 0.0001 * current_price if action in [1, 2, 3] else 0
        slippage = 0.00005 * current_price if action == 3 else 0 # 市價平倉懲罰
        
        net_pnl = pnl - trading_fee - slippage
        
        # 3. 核心：風險調整後報酬 (Risk-Adjusted Reward)
        # 我們不只獎勵賺錢，更要懲罰波動 (Volatility Penalty)
        # 這能讓 Agent 追求像優式冠軍施同學那樣穩定的夏普值 4.8
        vol_penalty = 0.5 * np.std(self.recent_returns) if len(self.recent_returns) > 10 else 0
        
        # 4. 加入「回撤懲罰」 (Drawdown Penalty)
        # 反映優式看重的「成長韌性」：避免策略在錯誤時產生巨大虧損
        dd_penalty = 0
        if self.current_equity < self.peak_equity:
            drawdown = (self.peak_equity - self.current_equity) / self.peak_equity
            dd_penalty = drawdown * 2.0 # 權重可調，體現對風險的零容忍
            
        final_reward = net_pnl - vol_penalty - dd_penalty
        
        return final_reward
