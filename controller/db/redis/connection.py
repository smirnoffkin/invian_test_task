from redis.asyncio import Redis

from controller.config import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
