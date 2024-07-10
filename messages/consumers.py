import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async  
from .models import Messages
from jobs.models import Job

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["user"].id
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        
        self.job_group_name = f"chat_{self.job_id}_{min(self.user_id, self.receiver_id)}_{max(self.user_id, self.receiver_id)}"

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

    async def save_message(self, sender_id, receiver_id, job_id, text):
        try:
            sender = self.scope['user']  # Assuming sender is the current authenticated user
            receiver = await self.get_receiver(receiver_id)
            job = await self.get_job(job_id)

            if sender and receiver and job:
                # Asynchronously create Messages object
                await self.create_message(sender, receiver, job, text)
        except (User.DoesNotExist, Job.DoesNotExist):
            return

    async def create_message(self, sender, receiver, job, text):
        # Convert synchronous create call to asynchronous
        create_message_async = sync_to_async(Messages.objects.create)
        message = await create_message_async(sender=sender, receiver=receiver, job=job, text=text)

        # Send message to room group
        await self.channel_layer.group_send(
            self.job_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender': message.sender.id,
                    'receiver': message.receiver.id,
                    'text': message.text,
                    'created_at': message.created_at.isoformat(),
                    'is_seen': message.is_seen,
                }
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['message']))

    async def get_receiver(self, receiver_id):
        try:
            return await User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return None

    async def get_job(self, job_id):
        try:
            return await Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return None
