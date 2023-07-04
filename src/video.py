import os
from googleapiclient.discovery import build


api_key: str = os.getenv('API_KEY_YouTube')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                     id=video_id
                                                                     ).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v='+self.video_id
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.likes_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
