import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        # Ensure user is authenticated
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data or '{}')
        message = data.get('message', '').strip()
        sender_id = self.scope['user'].id

        if not message:
            return

        # Persist message
        msg = await self._save_message(self.conversation_id, sender_id, message)

        # Broadcast to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': msg.content,
                'sender': msg.sender.username,
                'sender_id': msg.sender_id,
                'created_at': msg.created_at.isoformat(),
                'id': msg.id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def _save_message(self, conversation_id, sender_id, content):
        conv = Conversation.objects.get(pk=conversation_id)
        msg = Message.objects.create(conversation=conv, sender_id=sender_id, content=content)
        conv.touch()
        return msg
