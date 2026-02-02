import requests
import time
import os
import json
import csv
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Initialize Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

supabase = None
if url and key:
    try:
        supabase = create_client(url, key)
    except Exception as e:
        print(f"⚠️ Supabase Warning: {e}")

# Initialize CSV Logging
csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'market_depth_log.csv')
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'symbol', 'bid_price', 'ask_price', 'spread', 'imbalance'])

def fetch_binance_tick_and_save(symbol="ETHUSDT"):
    """
    Fetch Binance Perpetual L2 data.
    Saves to Local CSV (Primary) and Supabase (Secondary/Backup).
    """
    try:
        # Binance Futures API endpoint
        endpoint = f"https://fapi.binance.com/fapi/v1/depth?symbol={symbol}&limit=5"
        
        try:
            res = requests.get(endpoint, timeout=5)
            if res.status_code != 200:
                print(f"⚠️ API Error: {res.status_code} - {res.text}")
                return
            data = res.json()
        except Exception as e:
            print(f"⚠️ Network/API Error: {e}")
            return
        
        # Parse BBO
        bid_price = float(data['bids'][0][0])
        bid_qty = float(data['bids'][0][1])
        ask_price = float(data['asks'][0][0])
        ask_qty = float(data['asks'][0][1])
        
        spread = ask_price - bid_price
        imbalance = (bid_qty - ask_qty) / (bid_qty + ask_qty)
        timestamp = datetime.now().isoformat()

        print(f"📡 {symbol} | Bid: {bid_price} | Ask: {ask_price} | Spread: {spread:.4f} | Imbal: {imbalance:.4f}")

        # 1. Save to CSV (Robust)
        try:
            with open(csv_file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, symbol, bid_price, ask_price, spread, imbalance])
        except Exception as e:
            print(f"❌ CSV Error: {e}")

        # 2. Save to Supabase (Best Effort)
        if supabase:
            try:
                payload = {
                    "symbol": symbol,
                    "bid_price": bid_price,
                    "ask_price": ask_price,
                    "spread": spread,
                    "meta_data": {
                        "bid_qty": bid_qty,
                        "ask_qty": ask_qty,
                        "imbalance": imbalance,
                        "top_5_bids": data['bids'],
                        "top_5_asks": data['asks']
                    }
                }
                # Using best-effort insert
                supabase.table("market_depth_log").insert(payload).execute()
            except Exception as e:
                # Suppress verbose DB errors to keep console clean
                pass

    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting AlphaPulse Data Collector (Binance -> CSV + Supabase)")
    print("   Target: High-Frequency Order Book Data (ETH/USDT Perps)")
    print("   Press Ctrl+C to stop.")
    
    try:
        while True:
            fetch_binance_tick_and_save("ETHUSDT")
            time.sleep(2) 
    except KeyboardInterrupt:
        print("\n🛑 Collector Stopped.")
