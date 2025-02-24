import asyncio
import asyncpg
from app.config import DB_CONFIG, DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                host=DB_HOST,
                port=5432,
                max_size=10,  # Максимальное количество соединений в пуле
                min_size=1,   # Минимальное количество соединений
                timeout=30     # Таймаут на запрос
            )
        except Exception as e:
            print(f"Error connecting to the database: {e}")


    async def disconnect(self):
        if self.pool:
            await self.pool.close()

db = Database()