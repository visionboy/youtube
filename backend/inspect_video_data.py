import requests
import json

# Get a sample video from the API
r = requests.get('http://localhost:8000/api/tiktok/search', params={'q': 'dance', 'maxResults': 1})
data = r.json()

if data.get('videos'):
    video = data['videos'][0]
    print("=== Video Data Structure ===")
    print(json.dumps(video, indent=2))
    print("\n=== Key Fields ===")
    print(f"ID: {video.get('id')}")
    print(f"Title: {video.get('title')}")
    print(f"Thumbnail URL: {video.get('thumbnails', {}).get('medium', {}).get('url')}")
    print(f"View Count: {video.get('statistics', {}).get('viewCount')}")
    print(f"Like Count: {video.get('statistics', {}).get('likeCount')}")
    print(f"Comment Count: {video.get('statistics', {}).get('commentCount')}")
else:
    print("No videos found")
