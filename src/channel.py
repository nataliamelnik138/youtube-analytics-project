import json
import os
from googleapiclient.discovery import build
import isodate

api_key: str = os.getenv('API_KEY_YouTube')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel_id
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = 'https://www.youtube.com/channel/'+self.channel["items"][0]["id"]
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f"{self.title} ({self.url})"

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        # api_key: str = os.getenv('API_KEY_YouTube')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        data = self.__dict__
        del data['channel']
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)
    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)
