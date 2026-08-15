import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            logger.warning("WS_CONNECT | status=rejected | reason=unauthenticated")
            await self.close()
            return

        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info(f"WS_CONNECT | email={user.email} | status=success")

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if not user.is_anonymous:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            logger.info(f"WS_DISCONNECT | email={user.email} | code={close_code}")

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["data"]))
