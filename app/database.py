import tortoise
import tortoise.backends.base.client
import tortoise.transactions

from app.core.config import settings


async def initialize(generate_safe: bool = True) -> None:
    await tortoise.Tortoise.init(config=settings.TORTOISE.dict())


async def close_connections():
    await tortoise.Tortoise.close_connections()