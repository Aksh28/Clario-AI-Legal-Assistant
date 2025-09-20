import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
HF_KEY = os.getenv("HF_API_KEY")

if not HF_KEY:
    print("❌ No Hugging Face key found in .env")
    exit()

# Pick a free model (guaranteed working)
model_id = "google/flan-t5-small"

api_url = f"https://api-inference.huggingface.co/models/{model_id}"

headers = {"Authorization": f"Bearer {HF_KEY}"}

payload = {
    "inputs": "Summarize: The employee can be fired at will without pay.",
    "parameters": {"max_new_tokens": 100}
}

print("🔄 Sending request to Hugging Face...")

response = requests.post(api_url, headers=headers, json=payload)

if response.status_code == 200:
    print("✅ Hugging Face response:", response.json())
else:
    print(f"❌ Error {response.status_code}: {response.text}")
