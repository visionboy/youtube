from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional
from config import Settings

class YouTubeService:
    def __init__(self):
        pass
    
    def _get_youtube_client(self):
        """Get YouTube API client with current API key"""
        api_key = Settings.get_api_key()
        if not api_key:
            raise ValueError("YouTube API key not configured")
        return build('youtube', 'v3', developerKey=api_key)
    
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
        Search for videos using YouTube Data API
        
        Args:
            query: Search query string
            max_results: Maximum number of results (default: 25)
            order: Sort order (date, rating, relevance, viewCount)
        
        Returns:
            Dictionary with videos list and metadata
        """
        try:
            youtube = self._get_youtube_client()
            
            # Calculate publishedAfter date
            published_after_rfc = None
            if published_after:
                from datetime import datetime, timedelta
                now = datetime.utcnow()
                if published_after == "1m":
                    date = now - timedelta(days=30)
                elif published_after == "2m":
                    date = now - timedelta(days=60)
                elif published_after == "6m":
                    date = now - timedelta(days=180)
                elif published_after == "1y":
                    date = now - timedelta(days=365)
                
                if published_after != "all" and published_after in ["1m", "2m", "6m", "1y"]:
                    published_after_rfc = date.isoformat("T") + "Z"

            # Search for videos
            search_params = {
                'q': query,
                'part': 'id,snippet',
                'maxResults': max_results,
                'order': order,
                'type': 'video'
            }
            
            if published_after_rfc:
                search_params['publishedAfter'] = published_after_rfc
                
            if video_duration and video_duration != "any":
                search_params['videoDuration'] = video_duration
                
            if page_token:
                search_params['pageToken'] = page_token
                
            search_response = youtube.search().list(**search_params).execute()
            
            next_page_token = search_response.get('nextPageToken')
            
            # Get video IDs
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return {"videos": [], "total": 0}
            
            # Get video statistics and content details
            videos_response = youtube.videos().list(
                part='statistics,snippet,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            # Get channel IDs to fetch subscriber counts
            channel_ids = list(set(item['snippet']['channelId'] for item in videos_response.get('items', [])))
            
            # Fetch channel details
            channels_data = {}
            if channel_ids:
                channels_response = youtube.channels().list(
                    part='statistics',
                    id=','.join(channel_ids)
                ).execute()
                
                for item in channels_response.get('items', []):
                    channels_data[item['id']] = int(item['statistics'].get('subscriberCount', 0))
            
            # Format response and filter by ratio
            videos = []
            for item in videos_response.get('items', []):
                view_count = int(item['statistics'].get('viewCount', 0))
                channel_id = item['snippet']['channelId']
                subscriber_count = channels_data.get(channel_id, 0)
                
                # Calculate ratio
                ratio = 0
                if subscriber_count > 0:
                    ratio = (view_count / subscriber_count) * 100
                
                # Filter by min_ratio if specified
                if min_ratio is not None and ratio < min_ratio:
                    continue

                # Filter by min_comments if specified
                comment_count = int(item['statistics'].get('commentCount', 0))
                if min_comments is not None and comment_count < min_comments:
                    continue
                
                # Filter by tag if specified
                video_tags = item['snippet'].get('tags', [])
                if tag:
                    tag_lower = tag.lower()
                    if not any(t.lower() == tag_lower for t in video_tags):
                        continue
                    
                video_data = {
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channelTitle': item['snippet']['channelTitle'],
                    'publishedAt': item['snippet']['publishedAt'],
                    'thumbnails': item['snippet']['thumbnails'],
                    'tags': video_tags,
                    'statistics': {
                        'viewCount': view_count,
                        'likeCount': int(item['statistics'].get('likeCount', 0)),
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
                "nextPageToken": next_page_token
            }
            
        except HttpError as e:
            error_message = f"YouTube API error: {e.resp.status} - {e.content.decode()}"
            raise Exception(error_message)
        except Exception as e:
            raise Exception(f"Error searching videos: {str(e)}")
    
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific video
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Dictionary with video details or None if not found
        """
        if not self.youtube:
            raise ValueError("YouTube API key not configured")
        
        try:
            response = self.youtube.videos().list(
                part='statistics,snippet,contentDetails',
                id=video_id
            ).execute()
            
            items = response.get('items', [])
            if not items:
                return None
            
            item = items[0]
            return {
                'id': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channelTitle': item['snippet']['channelTitle'],
                'publishedAt': item['snippet']['publishedAt'],
                'thumbnails': item['snippet']['thumbnails'],
                'statistics': {
                    'viewCount': int(item['statistics'].get('viewCount', 0)),
                    'likeCount': int(item['statistics'].get('likeCount', 0)),
                    'commentCount': int(item['statistics'].get('commentCount', 0))
                }
            }
            
        except HttpError as e:
            error_message = f"YouTube API error: {e.resp.status} - {e.content.decode()}"
            raise Exception(error_message)
        except Exception as e:
            raise Exception(f"Error getting video details: {str(e)}")

youtube_service = YouTubeService()
