import requests
import time
from config import API_KEY, BASE_URL

HEADERS = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

def fetch_json(endpoint, params=None, retries=5):
    url = f"{BASE_URL}{endpoint}"
    backoff = 2

    for attempt in range(retries):
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 404:
            print(f"[SKIP] 404 Not Found: {endpoint}")
            return None

        elif response.status_code == 429:
            print(f"[RATE LIMIT] Sleeping {backoff}s...")
            time.sleep(backoff)
            backoff *= 2   # exponential backoff

        else:
            print(f"[ERROR] {response.status_code}: {response.text}")
            time.sleep(backoff)

    #NOT crash pipeline
    print(f"[FAILED] Skipping after retries: {endpoint}")
    return None
