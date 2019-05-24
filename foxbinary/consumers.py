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
        text_key = event.get('text', None)
        if text_key is not None:
            payload = json.loads(text_key)
        print(payload) 
        await self.send({
            "type": "websocket.send",
            "text": "recieved tick value",
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)
