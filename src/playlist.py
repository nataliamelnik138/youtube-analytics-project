from datetime import timedelta

import isodate

from src.channel import Channel


class PlayList(Channel):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_service().playlists().list(id=playlist_id, part='snippet,contentDetails', maxResults=50
                                                         ).execute().get('items')[0].get('snippet').get('title')

        # self.title
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    def get_video_information(self):
        """
        Возвращает словарь, содержащий данные по видеороликам в плейлисте
        """
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails', maxResults=50, ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)).execute()

        return video_response

    @property
    def total_duration(self):
        """
        Вычисляет сумарную длительность плейлиста
        :return: объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        video_response = self.get_video_information()
        length_time = timedelta()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            length_time += duration

        return length_time

    def show_best_video(self):
        """
        возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        max_likes_count = 0
        url_top_video = ''
        video_response = self.get_video_information()
        for video in video_response['items']:
            likes_count = int(video['statistics']['likeCount'])
            if likes_count > max_likes_count:
                max_likes_count = likes_count
                url_top_video = 'https://youtu.be/' + video['id']

        return url_top_video
