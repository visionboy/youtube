import requests
import json
from config import Settings

api_key = Settings.get_tiktok_api_key()
host = Settings().tiktok_rapidapi_host
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": host
}

print(f"1. Searching Challenge 'dance'...")
url = f"https://{host}/challenge/search"
params = {"keywords": "dance"}

try:
    response = requests.get(url, headers=headers, params=params, timeout=10)
    data = response.json()
    
    if 'data' in data and 'challenges' in data['data']:
        challenges = data['data']['challenges']
        print(f"Found {len(challenges)} challenges")
        
        if len(challenges) > 0:
            challenge = challenges[0]
            c_id = challenge.get('id')
            c_name = challenge.get('title') # or name?
            print(f"Using Challenge: {c_name} (ID: {c_id})")
            print(f"Challenge Keys: {list(challenge.keys())}")
            
            print(f"\n2. Getting Posts for Challenge {c_id}...")
            url_posts = f"https://{host}/challenge/posts"
            params_posts = {"challenge_id": c_id, "count": 2}
            
            resp_posts = requests.get(url_posts, headers=headers, params=params_posts, timeout=10)
            data_posts = resp_posts.json()
            print(f"Posts Response Keys: {list(data_posts.keys())}")
            
            if 'data' in data_posts:
                p_data = data_posts['data']
                print(f"Posts Data Type: {type(p_data)}")
                if isinstance(p_data, dict):
                    print(f"Posts Data Keys: {list(p_data.keys())}")
                    if 'videos' in p_data:
                        videos = p_data['videos']
                        print(f"Found {len(videos)} videos")
                        if len(videos) > 0:
                            print(f"First Video Keys: {list(videos[0].keys())}")
                            print(f"Video ID: {videos[0].get('video_id')}")
                            print(f"Aweme ID: {videos[0].get('aweme_id')}")
            
    else:
        print("No challenges found in structure")
        print(json.dumps(data, indent=2)[:500])

except Exception as e:
    print(f"Error: {e}")
