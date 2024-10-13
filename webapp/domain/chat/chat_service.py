from fastapi import WebSocket
from sqlalchemy import select
from webapp.common.exceptions import persistence
from webapp.domain.chat.channel_manager import ChannelManager
from webapp.common.util.id_generator import create_id
from webapp.domain.chat.chat import Message, User, Entry
from webapp.domain.user.entity.user import User as UserTable


class ChatService:
    def __init__(self, channel_manager: ChannelManager, session_context):
        self.session_context = session_context
        self.channel_manager = channel_manager

    def _get_user(self, user_id):
        with self.session_context() as session:
            stmt = select(UserTable).filter_by(id=user_id)
            user = session.execute(stmt).scalar_one()

        return user.id, user.nickname, user.profile_image_url

    # async def entry(self, group_id, user_id, websocket: WebSocket):
    #     try:
    #         channel = self.channel_manager.get_channel(group_id)
    #     except persistence.ResourceNotFound:
    #         channel = self.channel_manager.create_channel(group_id)
    #
    #     user_id, nickname, profile_image_url = self._get_user(user_id)
    #     channel.cache_user(user_id=user_id, nickname=nickname, profile_image_url=profile_image_url)
    #     session_id = create_id()
    #     await channel.connect(session_id=session_id, user_id=user_id, websocket=websocket)
    #     await channel.broadcast(
    #         Entry.create(
    #             user_id=user_id,
    #             nickname=nickname,
    #             profile_image_url=profile_image_url
    #         )
    #     )
    #
    #     return session_id

    async def connect(
            self,
            group_id: str,
            user_id: str,
            session_id: str | None,
            websocket: WebSocket
    ):
        try:
            channel = self.channel_manager.get_channel(group_id)
        except persistence.ResourceNotFound:
            channel = self.channel_manager.create_channel(group_id)

        if session_id is None:
            session_id = create_id()
        await channel.connect(user_id=user_id, session_id=session_id, websocket=websocket)

    async def disconnect(self, group_id: str, session_id: str):
        channel = self.channel_manager.get_channel(group_id)
        channel.disconnect(session_id)

    async def send_message(self, group_id: str, user_id: str, content: str):
        channel = self.channel_manager.get_channel(group_id)
        message = Message.create(user_id, content)
        await channel.broadcast(message)
