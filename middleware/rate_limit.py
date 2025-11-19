from aiogram import BaseMiddleware
from aiogram.types import Message
import time
class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, delay: float = 1.0):
        super().__init__(); self.delay = delay; self.last = {}
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            uid = event.from_user.id; now = time.time()
            if uid in self.last and now - self.last[uid] < self.delay:
                return
            self.last[uid] = now
        return await handler(event, data)
