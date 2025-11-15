"""
WebSocket Consumers for Real-Time Communication
Author: Cavin Otieno
Contact: cavin.otieno012@gmail.com
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Workflow, ProgressLog


class WorkflowConsumer(AsyncWebsocketConsumer):
    """Real-time workflow progress updates"""
    
    async def connect(self):
        self.workflow_id = self.scope['url_route']['kwargs']['workflow_id']
        self.room_group_name = f'workflow_{self.workflow_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'workflow_progress',
                'message': message
            }
        )

    async def workflow_progress(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


class ProgressConsumer(AsyncWebsocketConsumer):
    """Global progress tracking consumer"""
    
    async def connect(self):
        self.room_group_name = 'progress_updates'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def progress_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
