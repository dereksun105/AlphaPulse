# ⚡ AlphaPulse: Automated Quant Trading & RL Monitoring System

**AlphaPulse** is a high-performance quantitative trading dashboard and agent training system designed to demonstrate **"対弈本能" (Game Theory Instinct)** and **"敏捷反應" (Agile Response)**. It combines a rigorous Python Reinforcement Learning (RL) environment with a real-time Vue.js visualization dashboard.

This project integrates **Supabase Realtime** for instant data streaming, **Lightweight Charts** for professional financial visualization, and a custom **OpenAI Gym** environment for training agents with Sharpe-Ratio-guided rewards.

---

## 🚀 Features

- **🧠 Advanced RL Environment**: Custom `gym` environment (`TradingEnv`) simulating slippage, transaction costs, and volatility penalties.
- **📊 Real-Time Visualization**: Vue 3 + TypeScript dashboard streaming live training performance (Sharpe Ratio, MDD, Equity Curve).
- **⚡ U-Capital Style Dashboard**: Dark-mode, high-contrast aesthetics optimized for tracking "Strategy Growth" (2026 Plan).
- **💾 Supabase Cloud Sync**: Training data is seamlessly pushed to Supabase, enabling remote monitoring of local Python training sessions.

---

## 🛠️ Technology Stack

### **Frontend** (Visualization)

- **Framework**: Vue 3 (Composition API) + Vite
- **Charts**: TradingView Lightweight Charts (Canvas-based, high performance)
- **State Management**: Pinia
- **Database Integration**: `@supabase/supabase-js` (Realtime Subscriptions)
- **Language**: TypeScript

### **Backend / AI** (Training)

- **Environment**: Python `gymnasium`, `pandas`, `numpy`
- **RL Algorithm**: (Ready for) PPO / Stable Baselines3
- **Database Integration**: `supabase-py`

---

## 📂 Project Structure

```bash
AlphaPulse/
├── frontend/                 # Vue.js Dashboard
│   ├── src/components/       # TraderGrowthChart.vue (The Core Dashboard)
│   ├── src/stores/           # Pinia GrowthStore (Data Fetching)
│   └── ...
├── ops/                      # Database Operations
│   └── schema.sql            # Supabase Schema (trader_growth_log)
├── python/                   # RL Training Core
│   ├── trading_env.py        # Custom Gym Environment (Sharpe Logic)
│   ├── test_rl_upload.py     # Script to simulate/upload training data
│   └── requirements.txt      # Python dependencies
└── src/                      # TypeScript Utilities
    └── supabaseClient.ts     # Supabase connection
```

---

## 🏁 Getting Started

### 1. Database Setup (Supabase)

1.  Create a Supabase project.
2.  Run the SQL schema in `ops/schema.sql` in your Supabase SQL Editor to create the `trader_growth_log` table.
3.  Get your **URL** and **ANON KEY** from Project Settings.

### 2. Frontend Setup

Create a `.env` file in `frontend/`:

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

Install and Run:

```bash
cd frontend
npm install
npm run dev
```

> The dashboard will be available at `http://localhost:5173`.

### 3. RL Training Setup (Python)

Create a `.env` file in the root directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

Install Dependencies:

```bash
cd python
pip install -r requirements.txt
```

Run the Training Simulation:

```bash
python3 python/test_rl_upload.py
```

---

## 📈 Monitoring the Agent

1.  Open the **Frontend** in your browser.
2.  Run the **Python Script**.
3.  Watch the **Blue Growth Line** evolve in real-time as the agent "trades" and reports its Sharpe Ratio and Reward stats to the cloud.

---

## 🧪 Key Logic Highlights

**The Reward Function (Python)**:
To encourage stability (High Sharpe), the agent is penalized for volatility and drawdowns:

```python
reward = step_pnl - fee_penalty - (volatility * 1000) - (drawdown * 100)
```

**Real-Time Subscriptions (Vue)**:
The frontend does not poll. It uses WebSockets via Supabase:

```typescript
supabase.channel('growth-realtime')
  .on('postgres_changes', { event: 'INSERT', ... }, payload => {
      // Instant Chart Update
  })
```

---

_Built for the 2026 U-Capital Quantitative Challenge._
