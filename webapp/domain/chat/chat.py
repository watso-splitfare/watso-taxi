from fastapi import WebSocket
from dataclasses import dataclass
from datetime import datetime
from webapp.common.util.id_generator import create_id


@dataclass
class Chat:
    id: str
    timestamp: datetime
    type: str = 'CHAT'

    @staticmethod
    def _create(cls, type, **kwargs):
        return cls(
            id=create_id(),
            type=type,
            timestamp=datetime.now(),
            **kwargs
        )


@dataclass
class MetaData(Chat):
    users: list[dict] = None
    type: str = "METADATA"

    @classmethod
    def create(cls, users: list[dict]):
        return Chat._create(cls, cls.type, users=users)


@dataclass
class Message(Chat):
    user_id: str = None
    content: str = None
    type: str = "MESSAGE"

    @classmethod
    def create(cls, user_id, content):
        return Chat._create(cls, cls.type, user_id=user_id, content=content)


@dataclass
class Entry(Chat):
    user: dict = None
    type: str = "ENTRY"

    @classmethod
    def create(cls, user_id, nickname, profile_image_url):
        user = dict(id=user_id, nickname=nickname, profile_image_url=profile_image_url)
        return Chat._create(cls, cls.type, user=user)


@dataclass
class Exit(Chat):
    user_id: str = None
    type: str = "EXIT"

    @classmethod
    def create(cls, user_id):
        return Chat._create(cls, cls.type, user_id=user_id)


class Channel:
    def __init__(self, group_id):
        self.group_id = group_id
        self.websockets: dict[str, WebSocket] = {}

    def join(self, user_id: str, websocket: WebSocket):
        self.websockets[user_id] = websocket

    def quit(self, user_id):
        self.websockets.pop(user_id)

    async def send(self, chat: Chat):
        for user_id, websocket in self.websockets.items():
            await websocket.send_json(str(chat.__dict__))

    @property
    def member_ids(self) -> list[str]:
        return [key for key in self.websockets.keys()]
