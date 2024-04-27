from app.cache.redis import redis


class RegConfirmCodeCache:
    def __init__(self, user_id: int, code: str = None, expire_time: int = None):
        self.__key_name = f'reg_confirmation_code_id{user_id}'
        self.__code = code
        self.__expire_time = expire_time * 1000 if expire_time else None  # sec to msec

    async def save_code(self) -> None:
        await redis.set(name=self.__key_name, value=self.__code)
        if self.__expire_time:
            await redis.expire(name=self.__key_name, time=self.__expire_time)

    async def get_code(self) -> str | None:
        return await redis.get(self.__key_name)

    async def delete_code(self) -> None:
        await redis.delete(self.__key_name)
