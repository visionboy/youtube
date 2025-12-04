import requests
from config import Settings

api_key = Settings.get_tiktok_api_key()
host = Settings().tiktok_rapidapi_host
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": host
}

# Get videos
search_url = f"https://{host}/challenge/search"
response = requests.get(search_url, headers=headers, params={"keywords": "dance"}, timeout=10)
challenges = response.json()['data'].get('challenge_list', [])
challenge_id = challenges[0].get('id')

posts_url = f"https://{host}/challenge/posts"
response = requests.get(posts_url, headers=headers, params={"challenge_id": challenge_id, "count": 1}, timeout=15)
video = response.json()['data']['videos'][0]

print("Video IDs:")
print(f"  aweme_id: {video.get('aweme_id')}")
print(f"  video_id: {video.get('video_id')}")

print("\nPossible embed URLs:")
print(f"  Embed v2 (aweme_id): https://www.tiktok.com/embed/v2/{video.get('aweme_id')}")
print(f"  Embed (video_id): https://www.tiktok.com/embed/{video.get('video_id')}")

print("\nDirect video URLs:")
for key in video.keys():
    if 'play' in key.lower() or 'download' in key.lower():
        val = video[key]
        if isinstance(val, str) and ('http' in val or 'tiktok' in val):
            print(f"  {key}: {val[:80]}...")
