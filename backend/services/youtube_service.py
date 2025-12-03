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
        order: str = "relevance"
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
            
            # Search for videos
            search_response = youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                order=order,
                type='video'
            ).execute()
            
            # Get video IDs
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return {"videos": [], "total": 0}
            
            # Get video statistics
            videos_response = youtube.videos().list(
                part='statistics,snippet,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            # Format response
            videos = []
            for item in videos_response.get('items', []):
                video_data = {
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
                videos.append(video_data)
            
            return {
                "videos": videos,
                "total": len(videos),
                "query": query,
                "order": order
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
