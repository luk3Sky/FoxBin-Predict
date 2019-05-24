import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import SyncConsumer, AsyncConsumer

class BinaryConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
    	print("connected", event)
    	await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("recieved", event)
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)
