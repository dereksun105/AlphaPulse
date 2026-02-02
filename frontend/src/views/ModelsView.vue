<template>
  <div class="page-container">
    <header class="page-header">
      <h1>模型實驗室日誌</h1>
      <p class="subtitle">追蹤智能的演化軌跡</p>
    </header>

    <div class="timeline">
      
      <div class="entry current">
        <div class="date">Feb 2026 (當前)</div>
        <div class="content">
          <h3>🚀 AlphaPulse V3 - "剝頭皮策略 (The Scalper)"</h3>
          <span class="tag success">成功</span>
          <p>
            實作 <strong>Sharpe 導向獎勵 (Sharpe-Guided Reward)</strong> 是一個重大突破。
            模型不再追逐「幸運」的單次暴利，轉而重視穩定性。
            近期測試顯示，在 200 個 Epoch 中 Sharpe Ratio 穩定維持在 > 1.8。
            加入了滑價模擬後，模型學會了在成交量低迷時期避免交易。
          </p>
        </div>
      </div>

      <div class="entry">
        <div class="date">Jan 2026</div>
        <div class="content">
          <h3>🧪 Model B - "保守派 (SafeKeeper)"</h3>
          <span class="tag warning">已廢棄</span>
          <p>
            我們曾嘗試對<em>任何</em>虧損交易施加極重懲罰。
            <strong>結果：</strong> 代理人學會了「什麼都不做」。它選擇單純持有現金以避免任何懲罰。
            <strong>教訓：</strong> 獎勵函數必須鼓勵探索 (Exploration)，而不僅僅是恐懼。
          </p>
        </div>
      </div>

      <div class="entry">
        <div class="date">Dec 2025</div>
        <div class="content">
          <h3>💥 Model A - "DQN 基準 (Baseline)"</h3>
          <span class="tag danger">失敗</span>
          <p>
            最初嘗試使用標準 DQN 配合密集 PnL 獎勵。
            <strong>結果：</strong> 極度不穩定。代理人學會了在趨勢中過度槓桿，但當趨勢反轉時帳戶直接爆倉。
            回撤 (Drawdown) 超過 40%。這不符合 UC-Capital 的標準。
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.page-container {
  padding: 40px;
  max-width: 1000px;
  margin: 0 auto;
  color: #e0e0e0;
}

.page-header {
  margin-bottom: 60px;
  text-align: center;
}

h1 {
  font-size: 3rem;
  background: linear-gradient(to right, #00E676, #00B0FF);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 10px;
}

.subtitle {
  color: #888;
  font-size: 1.2rem;
  font-style: italic;
}

.timeline {
  position: relative;
  border-left: 2px solid #333;
  margin-left: 20px;
  padding-left: 40px;
}

.entry {
  margin-bottom: 50px;
  position: relative;
}

.entry::before {
  content: '';
  position: absolute;
  left: -49px;
  top: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #333;
  border: 4px solid #111;
}

.entry.current::before {
  background: #00E676;
  box-shadow: 0 0 15px #00E676;
}

.date {
  font-family: monospace;
  color: #666;
  margin-bottom: 8px;
}

.content {
  background: #1a1a1a;
  padding: 25px;
  border-radius: 8px;
  border: 1px solid #2b2b2b;
}

.entry.current .content {
  border-color: #00E676;
}

h3 {
  margin-top: 0;
  display: inline-block;
  margin-right: 15px;
  color: #fff;
}

.tag {
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 4px;
  text-transform: uppercase;
  font-weight: bold;
}

.tag.success { background: rgba(0, 230, 118, 0.2); color: #00E676; }
.tag.warning { background: rgba(255, 145, 0, 0.2); color: #FF9100; }
.tag.danger { background: rgba(255, 82, 82, 0.2); color: #FF5252; }

p {
  color: #aaa;
  line-height: 1.6;
  margin-bottom: 0;
}
</style>
