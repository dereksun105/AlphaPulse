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
        

        # Update Equity
        self.current_equity = self.balance + (self.positions * current_price)
        
        # Calculate Reward using User's Custom Logic
        # We need bid_ask_spread for valid calculation. Assuming spread is roughly related to volatility or fixed
        bid_ask_spread = current_price * 0.0002 # 0.02% spread estimate
        reward = self._calculate_reward(action, current_price, bid_ask_spread)
        
        # Track history for internal Volatility (kept for legacy/logging if needed)
        # _calculate_reward updates self.recent_returns
        
        self.current_step += 1
        terminated = self.current_step >= len(self.df) - 1
        truncated = False
        
        return self._next_observation(), reward, terminated, truncated, {}

    def _calculate_reward(self, action, current_price, bid_ask_spread):
        """
        這段邏輯展現了 Derek 對於「期望值」與「風險控管」的實戰洞察
        """
        # 1. 模擬滑價 (Slippage) 與手續費
        # 在高頻交易環境中，滑價是 Alpha 的殺手
        # 我們假設滑價為價差的 50% (觸發市價單的代價)
        slippage_cost = bid_ask_spread * 0.5 if action != 0 else 0
        fee_rate = 0.0001  # 萬分之一手續費
        transaction_cost = (current_price * fee_rate) + slippage_cost

        # 2. 計算原始盈虧 (PnL)
        # 根據你的 position 狀態計算 (1: Long, -1: Short, 0: Flat)
        last_price = self.df.iloc[self.current_step - 1]['close'] if self.current_step > 0 else current_price
        raw_pnl = self.positions * (current_price - last_price)
        
        # 3. 風險調整後的回報 (Risk-Adjusted Reward)
        # 我們不只獎勵賺錢，更要懲罰不穩定的波動
        # 目標是對標優式冠軍施同學的 Sharpe Ratio 4.8 標竿
        net_return = raw_pnl - transaction_cost
        
        # Ensure self.returns_history exists (we mapped it to self.recent_returns in __init__)
        self.recent_returns.append(net_return)
        
        volatility_penalty = 0
        if len(self.recent_returns) > 20:
            # 懲罰標準差，鼓勵 Agent 尋找穩定的獲利模式
            volatility_penalty = np.std(self.recent_returns[-20:]) * 0.1
        
        # 4. 回撤懲罰 (Drawdown Penalty)
        # 優式看重在「不確定性中精準校正」的能力，巨大的回撤代表校正失敗
        drawdown_penalty = 0
        
        self.peak_equity = max(self.peak_equity, self.current_equity)
        
        if self.current_equity < self.peak_equity:
            drawdown = (self.peak_equity - self.current_equity) / (self.peak_equity + 1e-9)
            drawdown_penalty = drawdown * 1.5 # 權重係數，反映對風險的厭惡

        # 最終獎勵函數
        reward = net_return - volatility_penalty - drawdown_penalty
        
        return reward
