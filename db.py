import asyncpg


DATABASE_URL='postgresql://botuser:mypassword@localhost:5432/cinemabot'

CREATE_USERS_SQL = """
CREATE TABLE IF NOT EXISTS users (
  user_id        BIGINT PRIMARY KEY,
  username       TEXT,
  favorite_movie TEXT
);
"""

UPDATE_USER = """
INSERT INTO users(user_id, username)
VALUES($1, $2)
ON CONFLICT (user_id) DO UPDATE
  SET username = EXCLUDED.username
"""

SET_FAVORITE = """
UPDATE users SET favorite_movie = $2
WHERE user_id = $1;
"""

GET_FAVORITE = """
SELECT favorite_movie FROM users WHERE user_id = $1;
"""


class DB:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    @classmethod
    async def create(cls, dsn: str) -> "DB":
        pool = await asyncpg.create_pool(dsn, min_size=1, max_size=5)
        async with pool.acquire() as conn:
            await conn.execute(CREATE_USERS_SQL)
        return cls(pool)
    
    async def upsert_user(self, user_id: int, username: str | None):
        async with self.pool.acquire() as conn:
            await conn.execute(UPDATE_USER, user_id, username)

    async def set_favorite(self, user_id: int, title: str) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(SET_FAVORITE, user_id, title)

    async def get_favorite(self, user_id: int) -> str | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(GET_FAVORITE, user_id)
        return row["favorite_movie"] if row and row["favorite_movie"] else None