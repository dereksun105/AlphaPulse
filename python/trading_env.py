import gymnasium as gym
import numpy as np
import pandas as pd
import random
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
        row = self.df.iloc[self.current_step]
        return np.array([row['open'], row['high'], row['low'], row['close'], row['volume']], dtype=np.float32)

    def step(self, action):
        prev_equity = self.current_equity
        current_price = self.df.iloc[self.current_step]['close']
        
        # --- EXECUTE ACTION & SLIPPAGE ---
        # 模擬滑價 (Slippage Simulation):
        # 每次交易不一定能成交在 close price，會受到市場深度影響 (Random Normal)
        # 這展現了對真實交易環境的理解
        actual_price = current_price
        if action in [1, 2, 3]: # Buy, Sell, or Close
            slippage_pct = np.abs(np.random.normal(0, 0.0002)) # Mean 0, Std 0.02%
            if action == 1: # Buy (Ask price higher)
                actual_price = current_price * (1 + slippage_pct)
            else: # Sell (Bid price lower)
                actual_price = current_price * (1 - slippage_pct)
        
        # Basic Trading Logic (Simplified)
        # 1=Buy (Add 1 unit), 2=Sell (Subtract 1 unit), 3=Close (Reset to 0)
        # Note: In real logic, we handle lots/margin. Here simplified to units.
        trade_units = 1
        
        if action == 1: # Buy
             cost = size = trade_units * actual_price
             self.balance -= cost
             # Weighted average entry price updating would go here
             if self.positions == 0: self.entry_price = actual_price
             self.positions += trade_units
             
        elif action == 2: # Sell (Short)
             gain = trade_units * actual_price
             self.balance += gain
             if self.positions == 0: self.entry_price = actual_price
             self.positions -= trade_units
             
        elif action == 3 and self.positions != 0: # Close All
             if self.positions > 0:
                 self.balance += self.positions * actual_price
             else:
                 self.balance -= abs(self.positions) * actual_price
             self.positions = 0
             self.entry_price = 0.0
        
        # Update Equity
        # Equity = Cash + Unrealized PnL
        # Unrealized PnL = PositionQuoteValue (for Long) or ... 
        # Simplified: Equity = Balance + (Positions * CurrentPrice)
        # Note: If Short, Positions is negative. 
        # Balance was increased when we Sold Short. 
        # So Balance + (-10 * Price) correctly reduces Equity if Price goes up.
        
        self.current_equity = self.balance + (self.positions * current_price)
        self.peak_equity = max(self.peak_equity, self.current_equity)
        
        # Calculate Step Return (Change in Equity)
        step_pnl = self.current_equity - prev_equity
        
        # --- USER'S REWARD LOGIC (SHARPE GUIDED) ---
        reward = self._get_reward(step_pnl, action)
        # -------------------------------------------
        
        # Track history for Volatility
        pct_return = step_pnl / prev_equity if prev_equity != 0 else 0
        self.recent_returns.append(pct_return)
        if len(self.recent_returns) > self.returns_window:
            self.recent_returns.pop(0)

        self.current_step += 1
        terminated = self.current_step >= len(self.df) - 1
        truncated = False
        
        return self._next_observation(), reward, terminated, truncated, {}

    def _get_reward(self, step_pnl, action):
        """
        這段邏輯展現了 Derek 對於「期望值」與「風險控管」的洞察力
        """
        # 1. 交易成本懲罰 (Trading Cost)
        # 頻繁交易會被手續費吃掉利潤，這是新手最常犯的錯誤
        fee_penalty = 0
        if action in [1, 2, 3]:
            fee_penalty = 5.0 # Fixed cost per trade or %

        # 2. 波動懲罰 (Volatility Penalty) -> 模擬夏普值的分母
        # 我們希望 Agent 不只是賺錢，還要賺得「穩」
        volatility = np.std(self.recent_returns) if len(self.recent_returns) > 5 else 0
        risk_penalty = volatility * 1000.0 # 係數需要 Tuning

        # 3. 回撤懲罰 (Drawdown Penalty)
        # 這是優式資本極為看重的指標：MDD (Max Drawdown)
        drawdown = (self.peak_equity - self.current_equity) / self.peak_equity
        dd_penalty = drawdown * 100.0 

        # Final Reward Logic:
        # PnL - (Costs + Risk + Drawdown)
        reward = step_pnl - fee_penalty - risk_penalty - dd_penalty
        
        return reward
