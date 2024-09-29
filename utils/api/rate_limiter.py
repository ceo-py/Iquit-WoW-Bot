import time
import asyncio
from settings import MAX_REQUESTS_PER_MINUTE, WAITING_TIME


REFILL_RATE = MAX_REQUESTS_PER_MINUTE / WAITING_TIME


class RateLimiter:
    def __init__(self):
        self.tokens = MAX_REQUESTS_PER_MINUTE
        self.last_refill = time.time()

    async def wait_for_token(self):
        while self.tokens < 1:
            self.refill()
            await asyncio.sleep(0.1)
        self.tokens -= 1

    def refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(MAX_REQUESTS_PER_MINUTE, self.tokens + elapsed * REFILL_RATE)
        self.last_refill = now


rate_limiter = RateLimiter()
