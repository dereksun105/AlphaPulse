# ⚡ AlphaPulse: 自動化量化交易與 RL 監控系統

**AlphaPulse** 是一個高性能的量化交易儀表板與代理人訓練系統，旨在展示 **「對弈本能」(Game Theory Instinct)** 與 **「敏捷反應」(Agile Response)**。本專案結合了嚴謹的 Python 強化學習 (RL) 環境與即時的 Vue.js 視覺化儀表板。

我們整合了 **Supabase Realtime** 實現數據即時串流，使用 **Lightweight Charts** 進行專業金融視覺化，並構建了客製化的 **OpenAI Gym** 環境，致力於訓練出以 Sharpe Ratio 為導向的智能代理人。

---

## 🚀 功能特色

- **🧠 進階 RL 環境**: 客製化的 `gym` 環境 (`TradingEnv`)，模擬了滑價 (Slippage)、交易成本與波動性懲罰。
- **📊 如果視覺化**: Vue 3 + TypeScript 儀表板，即時串流訓練成效 (Sharpe Ratio, MDD, Equity Curve)。
- **⚡ UC-Capital 風格儀表板**: 深色模式、高對比美學，專為追蹤「策略成長」(2026 計畫) 而優化。
- **💾 Supabase 雲端同步**: 訓練數據無縫推送到 Supabase，實現對本地 Python 訓練任務的遠端監控。

---

## 🛠️ 技術棧

### **前端 (Frontend)** (視覺化)

- **框架**: Vue 3 (Composition API) + Vite
- **圖表**: TradingView Lightweight Charts (基於 Canvas，高性能)
- **狀態管理**: Pinia
- **資料庫整合**: `@supabase/supabase-js` (Realtime 訂閱)
- **語言**: TypeScript

### **後端 / AI (Backend)** (訓練核心)

- **環境**: Python `gymnasium`, `pandas`, `numpy`
- **RL 演算法**: (支援) PPO / Stable Baselines3
- **資料庫整合**: `supabase-py`

---

## 📂 專案結構

```bash
AlphaPulse/
├── frontend/                 # Vue.js 儀表板
│   ├── src/components/       # TraderGrowthChart.vue (核心圖表元件)
│   ├── src/stores/           # Pinia GrowthStore (數據獲取)
│   └── ...
├── ops/                      # 資料庫運維
│   └── schema.sql            # Supabase Schema (trader_growth_log 表結構)
├── python/                   # RL 訓練核心
│   ├── trading_env.py        # 客製化 Gym 環境 (夏普邏輯)
│   ├── test_rl_upload.py     # 模擬/上傳訓練數據腳本
│   └── requirements.txt      # Python 依賴
└── src/                      # TypeScript 工具庫
    └── supabaseClient.ts     # Supabase 連線設定
```

---

## 🏁 快速開始 (Getting Started)

### 1. 資料庫設定 (Supabase)

1.  建立一個 Supabase 專案。
2.  在 Supabase SQL Editor 中執行 `ops/schema.sql`，建立 `trader_growth_log` 資料表。
3.  從 Project Settings 獲取你的 **URL** 和 **ANON KEY**。

### 2. 前端設定

在 `frontend/` 目錄下建立 `.env` 檔案：

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

安裝並執行：

```bash
cd frontend
npm install
npm run dev
```

> 儀表板將在 `http://localhost:5173` 啟動。

### 3. RL 訓練設定 (Python)

在根目錄下建立 `.env` 檔案：

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

安裝依賴：

```bash
cd python
pip install -r requirements.txt
```

執行訓練模擬：

```bash
python3 python/test_rl_upload.py
```

---

## 📈 如何監控代理人

1.  在瀏覽器中打開 **前端儀表板**。
2.  執行 **Python 腳本**。
3.  觀察 **藍色成長曲線** 隨時間即時變化，代理人將在雲端回報其夏普值 (Sharpe Ratio) 與回報數據。

---

## 🧪 核心邏輯解析

**獎勵函數 (Python)**:
為了鼓勵穩定性 (高 Sharpe)，我們對波動性和回撤進行懲罰：

```python
reward = step_pnl - fee_penalty - (volatility * 1000) - (drawdown * 100)
```

**即時訂閱 (Vue)**:
前端不使用輪詢 (Polling)，而是透過 Supabase WebSocket 實現：

```typescript
supabase.channel('growth-realtime')
  .on('postgres_changes', { event: 'INSERT', ... }, payload => {
      // 圖表即時更新
  })
```

---

_專為 2026 UC-Capital 量化挑戰打造。_
