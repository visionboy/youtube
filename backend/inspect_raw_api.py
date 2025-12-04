import requests
from config import Settings

api_key = Settings.get_tiktok_api_key()
host = Settings().tiktok_rapidapi_host
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": host
}

# Step 1: Search for challenge
search_url = f"https://{host}/challenge/search"
response = requests.get(search_url, headers=headers, params={"keywords": "dance"}, timeout=10)
search_data = response.json()

challenges = search_data['data'].get('challenge_list', [])
if challenges:
    challenge_id = challenges[0].get('id')
    print(f"Challenge ID: {challenge_id}")
    
    # Step 2: Get videos
    posts_url = f"https://{host}/challenge/posts"
    response = requests.get(posts_url, headers=headers, params={"challenge_id": challenge_id, "count": 1}, timeout=15)
    data = response.json()
    
    if 'data' in data and 'videos' in data['data']:
        videos = data['data']['videos']
        if videos:
            video = videos[0]
            print("\n=== Raw Video Item Keys ===")
            print(list(video.keys()))
            
            print("\n=== Statistics ===")
            stats = video.get('statistics', {}) or video.get('stats', {})
            print(f"Stats keys: {list(stats.keys())}")
            print(f"Play count: {stats.get('playCount', stats.get('play_count', stats.get('play', 'N/A')))}")
            print(f"Digg count: {stats.get('diggCount', stats.get('digg_count', stats.get('likes', 'N/A')))}")
            print(f"Comment count: {stats.get('commentCount', stats.get('comment_count', stats.get('comments', 'N/A')))}")
            
            print("\n=== Video Info ===")
            video_info = video.get('video', {})
            print(f"Video keys: {list(video_info.keys())}")
            print(f"Cover: {video_info.get('cover', 'N/A')}")
            
            print("\n=== Author ===")
            author = video.get('author', {})
            print(f"Author keys: {list(author.keys())}")
            print(f"Nickname: {author.get('nickname', 'N/A')}")
            print(f"Follower count: {author.get('followerCount', author.get('follower_count', 'N/A'))}")
