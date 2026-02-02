import os
import random
import time
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables (assumes .env is in project root)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    raise ValueError("Supabase URL or Key is missing. Please check your .env file.")

supabase: Client = create_client(url, key)

def mock_train_and_upload():
    print("Starting mock training session...")
    
    # Get current max epoch to avoid duplicates in chart
    try:
        max_epoch_response = supabase.table("trader_growth_log") \
            .select("epoch") \
            .order("epoch", desc=True) \
            .limit(1) \
            .execute()
        
        start_epoch = 1
        if max_epoch_response.data and len(max_epoch_response.data) > 0:
            start_epoch = max_epoch_response.data[0]['epoch'] + 1
            print(f"Resuming from epoch {start_epoch}...")
            
    except Exception as e:
        print(f"Error fetching max epoch: {e}, starting from 1")
        start_epoch = 1

    # Simulate a training loop where we get stats every "epoch"
    for i in range(5):
        epoch = start_epoch + i
        # Simulate stats (Mocking PPO training metrics)
        sharpe_ratio = random.uniform(0.5, 2.5)
        mdd = random.uniform(0.05, 0.30)
        reward = random.uniform(50, 200) + (epoch * 10) # improving reward
        
        data = {
            "epoch": epoch,
            "sharpe_ratio": round(sharpe_ratio, 4),
            "mdd": round(mdd, 4),
            "reward": round(reward, 2)
        }
        
        print(f"Epoch {epoch}: Uploading stats - {data}")
        
        try:
            response = supabase.table("trader_growth_log").insert(data).execute()
            # print("Upload success:", response)
        except Exception as e:
            print(f"Error uploading: {e}")
            
        time.sleep(1) # Simulate training time

if __name__ == "__main__":
    mock_train_and_upload()
