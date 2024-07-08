import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Messages
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        # self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.job_group_name = f"chat_{self.user_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.job_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.job_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)
        sender_id = message["sender_id"]
        receiver_id = message['receiver_id']
        job_id = message['job_id']
        text = message['text']

        await self.save_message(sender_id, receiver_id, job_id, text)

    async def save_message(self, sender_id, receiver_id, job_id,  text):
        try:
            receiver_id = User.objects.get(id=receiver_id)
            sender_id = self.user_id
            message = Messages.objects.create(sender=sender_id, receiver=receiver_id, job_id=job_id, text=text)
            message.save()
        except User.DoesNotExist:
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.job_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender': message.sender,
                    'receiver': message.receiver,
                    'text': message.text,
                    'created_at': message.created_at.isoformat(),
                    'is_seen': message.is_seen,
                }
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['message']))
