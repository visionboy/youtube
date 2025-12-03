import requests
import json
from config import Settings

api_key = Settings.get_tiktok_api_key()
host = Settings().tiktok_rapidapi_host
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": host
}

query = "dance"

# Step 1: Search for challenge
print(f"Searching for challenge: {query}")
url = f"https://{host}/challenge/search"
response = requests.get(url, headers=headers, params={"keywords": query})

if response.status_code != 200:
    print(f"Failed to search challenge: {response.status_code}")
    exit(1)

data = response.json()
print(f"Response keys: {list(data.keys())}")
challenges = data.get('data', [])
print(f"Challenges type: {type(challenges)}")
if isinstance(challenges, list):
    print(f"Challenges count: {len(challenges)}")
elif isinstance(challenges, dict):
    print(f"Challenges keys: {list(challenges.keys())}")
else:
    print(f"Challenges content: {challenges}")

if not challenges:
    print("No challenges found")
    exit(1)

first_challenge = challenges[0]
challenge_id = first_challenge.get('id')
challenge_name = first_challenge.get('name')
print(f"Found challenge: {challenge_name} (ID: {challenge_id})")

# Step 2: Get videos for challenge
print(f"Getting videos for challenge ID: {challenge_id}")
url = f"https://{host}/challenge/posts"
response = requests.get(url, headers=headers, params={"challenge_id": challenge_id, "count": 5})

if response.status_code != 200:
    print(f"Failed to get videos: {response.status_code}")
    exit(1)

data = response.json()
videos = data.get('data', {}).get('videos', [])
print(f"Found {len(videos)} videos")

if videos:
    print(f"First video ID: {videos[0].get('video_id')}")
    print(f"First video Title: {videos[0].get('title')}")
