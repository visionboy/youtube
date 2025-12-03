import requests
import json
from config import Settings

api_key = Settings.get_tiktok_api_key()
host = Settings().tiktok_rapidapi_host

print(f"Using API key: {api_key[:10]}...")
print(f"Host: {host}")

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": host
}

# Try to find a working endpoint
tests = [
    # Try to search for a challenge/hashtag first
    ("/challenge/search", {"keywords": "dance"}),
    ("/search/challenge", {"keywords": "dance"}),
    ("/hashtag/search", {"keywords": "dance"}),
    
    # Try to use challenge/posts with different params
    ("/challenge/posts", {"challenge_name": "dance"}),
    ("/challenge/posts", {"keyword": "dance"}),
    ("/challenge/posts", {"hashtag": "dance"}),
    
    # Try user search
    ("/user/search", {"keywords": "dance"}),
]

for endpoint, params in tests:
    url = f"https://{host}{endpoint}"
    print(f"\nTesting: {url} with {params}")
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.text[:200]}")
        else:
            print(f"Error: {response.text[:100]}")
    except Exception as e:
        print(f"Exception: {e}")
