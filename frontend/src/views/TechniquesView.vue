<template>
  <div class="page-container">
    <header class="page-header">
      <h1>核心技術詳解</h1>
      <p class="subtitle">AlphaPulse 背後的工程架構</p>
    </header>

    <div class="content-grid">
      <section class="card">
        <h2>🧠 Proximal Policy Optimization (PPO)</h2>
        <p>
          我們採用 <strong>PPO</strong>，這是一種最先進的策略梯度 (Policy Gradient) 方法。不同於 Deep Q-Networks (DQN) 在連續動作空間中的掙扎或收斂不穩定，PPO 透過截斷策略更新 (Clipping Policy Updates) 提供了穩定的學習曲線。這確保了我們的代理人 (Agent) 在激進優化的過程中不會「遺忘」已習得的獲利策略。
        </p>
      </section>

      <section class="card">
        <h2>⚖️ Sharpe 導向獎勵函數</h2>
        <p>
          一個純粹追求利潤的代理人只是個賭徒。為了讓 <strong>UC-Capital (優式資本)</strong> 印象深刻，我們實作了客製化的獎勵函數：
        </p>
        <div class="code-block">
          Reward = Net_PnL - (Volatility * 0.1) - (Max_Drawdown * 1.5)
        </div>
        <p>
          這迫使代理人自我懲罰波動性。它將學會：一個 10% 回報但只有 2% 回撤的策略，優於一個 20% 回報但伴隨 50% 回撤的策略。
        </p>
      </section>

      <section class="card">
        <h2>📉 真實滑價模擬 (Slippage Simulation)</h2>
        <p>
          真實市場並非毫無摩擦。我們的 <code>TradingEnv</code> 模擬了：
        </p>
        <ul>
          <li><strong>買賣價差 (Bid-Ask Spread):</strong> 模擬每筆交易 0.02% 的成本。</li>
          <li><strong>執行延遲:</strong> 透過隨機價格偏差進行模擬。</li>
          <li><strong>交易手續費:</strong> 0.01% 的標準券商費用。</li>
        </ul>
        <p>這確保了我們挖掘出的 "Alpha" 足夠強健，能夠在實盤部署中存活。</p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  color: #e0e0e0;
}

.page-header {
  margin-bottom: 50px;
  text-align: center;
}

h1 {
  font-size: 3rem;
  background: linear-gradient(to right, #2962FF, #2196f3);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 10px;
}

.subtitle {
  color: #888;
  font-size: 1.2rem;
  letter-spacing: 1px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.card {
  background: #1e1e1e;
  padding: 30px;
  border-radius: 12px;
  border: 1px solid #333;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.5);
  border-color: #2962FF;
}

h2 {
  color: #fff;
  font-size: 1.5rem;
  margin-bottom: 15px;
  border-bottom: 2px solid #2962FF;
  display: inline-block;
  padding-bottom: 5px;
}

p, li {
  line-height: 1.6;
  color: #bbb;
}

ul {
  padding-left: 20px;
}

.code-block {
  background: #111;
  padding: 15px;
  border-radius: 6px;
  font-family: 'SF Mono', 'Fira Code', monospace;
  color: #00E676;
  margin: 15px 0;
  border-left: 3px solid #00E676;
}
</style>
