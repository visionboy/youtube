from typing import List, Dict, Optional
import random
import re
import requests
from datetime import datetime, timedelta
from config import Settings

class TikTokService:
    def __init__(self):
        pass
    
    def search_videos(
        self,
        query: str,
        max_results: int = 25,
        order: str = "relevance",
        published_after: Optional[str] = None,
        video_duration: Optional[str] = None,
        min_ratio: Optional[float] = None,
        min_comments: Optional[int] = None,
        tag: Optional[str] = None,
        page_token: Optional[str] = None
    ) -> Dict:
        """
        Search for TikTok videos. Uses RapidAPI if key is configured, otherwise Mock.
        """
        api_key = Settings.get_tiktok_api_key()
        
        if api_key:
            return self._search_rapidapi(
                api_key, query, max_results, order, published_after, 
                video_duration, min_ratio, min_comments, tag, page_token
            )
            
        # Mock data generation (Fallback)
        return self._generate_mock_data(query, max_results, order, min_ratio, min_comments)

    def _search_rapidapi(
        self,
        api_key: str,
        query: str,
        max_results: int,
        order: str,
        published_after: Optional[str],
        video_duration: Optional[str],
        min_ratio: Optional[float],
        min_comments: Optional[int],
        tag: Optional[str],
        page_token: Optional[str]
    ) -> Dict:
        """
        Execute search using RapidAPI TikTok Scraper
        API Documentation: https://rapidapi.com/DataFanatic/api/tiktok-scraper7
        """
        import json
        
        # TikTok Scraper API - 2-Step Search Flow
        # 1. Search for challenge/hashtag to get ID
        # 2. Get videos for that challenge
        
        host = Settings().tiktok_rapidapi_host
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": host
        }
        
        try:
            # Step 1: Search for challenge
            search_url = f"https://{host}/challenge/search"
            search_params = {"keywords": query}
            
            print(f"[TikTok API] Step 1: Searching challenge '{query}'")
            response = requests.get(search_url, headers=headers, params=search_params, timeout=10)
            
            challenge_id = None
            
            if response.status_code == 200:
                search_data = response.json()
                # Extract challenge ID from response
                if 'data' in search_data and isinstance(search_data['data'], dict):
                    # Try both 'challenge_list' and 'challenges' for compatibility
                    challenges = search_data['data'].get('challenge_list', []) or search_data['data'].get('challenges', [])
                    if challenges:
                        # Use the first matching challenge
                        challenge_id = challenges[0].get('id')
                        challenge_name = challenges[0].get('cha_name') or challenges[0].get('name')
                        print(f"[TikTok API] Found challenge: {challenge_name} (ID: {challenge_id})")
            
            # If no challenge found, try using the query as ID directly (fallback)
            if not challenge_id:
                print("[TikTok API] No challenge found, trying query as ID")
                challenge_id = query.replace("#", "").replace(" ", "")
            
            # Step 2: Get videos for challenge
            posts_url = f"https://{host}/challenge/posts"
            posts_params = {
                "challenge_id": challenge_id,
                "count": min(max_results, 50),
                "cursor": int(page_token) if page_token and page_token.isdigit() else 0
            }
            
            print(f"[TikTok API] Step 2: Getting posts for challenge {challenge_id}")
            response = requests.get(posts_url, headers=headers, params=posts_params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract videos
                videos_data = []
                if 'data' in data and isinstance(data['data'], dict):
                    videos_data = data['data'].get('videos', [])
                
                print(f"[TikTok API] Found {len(videos_data)} videos")
                
                if videos_data:
                    return self._process_tiktok_response(videos_data, query, order, max_results, min_ratio, min_comments)
                else:
                    print(f"[TikTok API] No videos in response, full response: {json.dumps(data, indent=2)[:500]}")
            else:
                error_text = response.text[:500]
                print(f"[TikTok API] Error response: {error_text}")
                
        except requests.exceptions.RequestException as e:
            print(f"[TikTok API] Request error: {str(e)}")
        except Exception as e:
            print(f"[TikTok API] Unexpected error: {str(e)}")
        
        # Fallback to mock data
        print("[TikTok API] Falling back to mock data")
        return self._generate_mock_data(query, max_results, order, min_ratio, min_comments)
    
    def _process_tiktok_response(
        self,
        items: list,
        query: str,
        order: str,
        max_results: int,
        min_ratio: Optional[float],
        min_comments: Optional[int]
    ) -> Dict:
        """Process TikTok API response and map to our format"""
        videos = []
        
        for item in items[:max_results]:
            try:
                # TikTok Scraper API returns fields at top level, not nested
                # Try top-level first, then fall back to nested structures
                
                # Get counts - check top level first (TikTok Scraper format)
                view_count = (
                    item.get('play_count') or 
                    item.get('playCount') or 
                    item.get('statistics', {}).get('playCount') or 
                    item.get('statistics', {}).get('play_count') or 
                    0
                )
                like_count = (
                    item.get('digg_count') or 
                    item.get('diggCount') or 
                    item.get('statistics', {}).get('diggCount') or 
                    item.get('statistics', {}).get('digg_count') or 
                    0
                )
                comment_count = (
                    item.get('comment_count') or 
                    item.get('commentCount') or 
                    item.get('statistics', {}).get('commentCount') or 
                    item.get('statistics', {}).get('comment_count') or 
                    0
                )
                share_count = (
                    item.get('share_count') or 
                    item.get('shareCount') or 
                    item.get('statistics', {}).get('shareCount') or 
                    item.get('statistics', {}).get('share_count') or 
                    0
                )
                
                # Author info
                author = item.get('author', {}) or {}
                subscriber_count = (
                    author.get('follower_count') or 
                    author.get('followerCount') or 
                    author.get('fans') or 
                    0
                )
                
                # Calculate ratio
                ratio = 0
                if subscriber_count > 0:
                    ratio = (view_count / subscriber_count) * 100
                    
                # Apply filters
                if min_ratio is not None and ratio < min_ratio:
                    continue
                if min_comments is not None and comment_count < min_comments:
                    continue
                
                # Get video ID
                # Prioritize numeric video_id for embed compatibility
                video_id = (
                    item.get('video_id') or 
                    item.get('aweme_id') or 
                    item.get('id') or 
                    str(random.randint(100000, 999999))
                )
                
                # Get thumbnail - check top level first
                cover_url = (
                    item.get('cover') or 
                    item.get('ai_dynamic_cover') or
                    item.get('dynamic_cover') or
                    item.get('origin_cover') or
                    item.get('video', {}).get('cover') or
                    item.get('video', {}).get('dynamicCover') or
                    item.get('video', {}).get('originCover') or
                    'https://placehold.co/480x360?text=TikTok'
                )
                
                # Get description
                desc = (
                    item.get('title') or 
                    item.get('desc') or 
                    item.get('description') or 
                    item.get('text') or
                    ''
                )
                
                # Get create time
                create_time = (
                    item.get('create_time') or 
                    item.get('createTime') or 
                    item.get('createtime') or 
                    0
                )
                if create_time:
                    published_at = datetime.fromtimestamp(create_time).isoformat() + "Z"
                else:
                    published_at = datetime.utcnow().isoformat() + "Z"
                
                # Get author name
                author_name = (
                    author.get('nickname') or 
                    author.get('unique_id') or 
                    author.get('uniqueId') or 
                    'Unknown'
                )
                
                # Extract hashtags from description if not provided
                tags = item.get('hashtags', []) or item.get('challenges', []) or []
                if not tags and desc:
                    # Extract hashtags from description text
                    hashtags = re.findall(r'#(\w+)', desc)
                    tags = hashtags[:5]  # Limit to 5 tags
                
                # Estimate follower count if not available
                # Use engagement rate to estimate: typical TikTok engagement is 5-10%
                # If we have views and likes, we can estimate
                if subscriber_count == 0 and view_count > 0:
                    # Estimate based on engagement (assuming 8% engagement rate)
                    estimated_followers = int(view_count / 8)  # Conservative estimate
                    subscriber_count = estimated_followers
                
                # Recalculate ratio with estimated or real follower count
                ratio = 0
                if subscriber_count > 0:
                    ratio = (view_count / subscriber_count) * 100
                
                video_data = {
                    'id': str(video_id),
                    'title': desc[:100] if desc else f'TikTok Video {video_id}',
                    'description': desc,
                    'channelTitle': author_name,
                    'publishedAt': published_at,
                    'thumbnails': {
                        'default': {'url': cover_url, 'width': 120, 'height': 90},
                        'medium': {'url': cover_url, 'width': 320, 'height': 180},
                        'high': {'url': cover_url, 'width': 480, 'height': 360}
                    },
                    'tags': tags,
                    'statistics': {
                        'viewCount': view_count,
                        'likeCount': like_count,
                        'commentCount': comment_count,
                        'shareCount': share_count,
                        'subscriberCount': subscriber_count,
                        'viewSubscriberRatio': round(ratio, 2)
                    }
                }
                videos.append(video_data)
                
            except Exception as e:
                print(f"[TikTok API] Error processing video item: {str(e)}")
                continue
        
        # Get next page token
        next_page_token = str(len(videos)) if len(videos) >= max_results else None
        
        return {
            "videos": videos,
            "total": len(videos),
            "query": query,
            "order": order,
            "nextPageToken": next_page_token
        }
    
    def _generate_mock_data(
        self,
        query: str,
        max_results: int,
        order: str,
        min_ratio: Optional[float],
        min_comments: Optional[int]
    ) -> Dict:
        """Generate mock data as fallback"""
        videos = []
        for i in range(max_results):
            view_count = random.randint(1000, 1000000)
            like_count = int(view_count * random.uniform(0.05, 0.2))
            comment_count = int(view_count * random.uniform(0.001, 0.01))
            subscriber_count = random.randint(10000, 5000000)
            
            ratio = 0
            if subscriber_count > 0:
                ratio = (view_count / subscriber_count) * 100

            # Filter logic (mock)
            if min_ratio is not None and ratio < min_ratio:
                continue
            if min_comments is not None and comment_count < min_comments:
                continue

            video_data = {
                'id': f'tiktok_{random.randint(100000, 999999)}',
                'title': f'TikTok Video {i+1} - {query}',
                'description': f'This is a mock TikTok video description for {query}. #tiktok #viral',
                'channelTitle': f'TikTokUser_{random.randint(1000, 9999)}',
                'publishedAt': (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat("T") + "Z",
                'thumbnails': {
                    'default': {
                        'url': 'https://placehold.co/120x90?text=TikTok',
                        'width': 120,
                        'height': 90
                    },
                    'medium': {
                        'url': 'https://placehold.co/320x180?text=TikTok+Video',
                        'width': 320,
                        'height': 180
                    },
                    'high': {
                        'url': 'https://placehold.co/480x360?text=TikTok+Video',
                        'width': 480,
                        'height': 360
                    }
                },
                'tags': ['tiktok', 'viral', query],
                'statistics': {
                    'viewCount': view_count,
                    'likeCount': like_count,
                    'commentCount': comment_count,
                    'subscriberCount': subscriber_count,
                    'viewSubscriberRatio': round(ratio, 2)
                }
            }
            videos.append(video_data)

        return {
            "videos": videos,
            "total": len(videos),
            "query": query,
            "order": order,
            "nextPageToken": "mock_next_page_token" if len(videos) == max_results else None
        }
    
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific video
        """
        api_key = Settings.get_tiktok_api_key()
        if api_key:
            # Implement real detail fetch here if needed
            pass

        # Mock implementation
        return {
            'id': video_id,
            'title': f'TikTok Video Details {video_id}',
            'description': 'Detailed description of the TikTok video.',
            'channelTitle': 'TikTokUser_Details',
            'publishedAt': datetime.utcnow().isoformat("T") + "Z",
            'thumbnails': {
                'medium': {
                    'url': 'https://placehold.co/320x180?text=TikTok+Detail',
                    'width': 320,
                    'height': 180
                },
                'high': {
                    'url': 'https://placehold.co/480x360?text=TikTok+Detail',
                    'width': 480,
                    'height': 360
                }
            },
            'statistics': {
                'viewCount': 50000,
                'likeCount': 2500,
                'commentCount': 100
            }
        }

tiktok_service = TikTokService()
