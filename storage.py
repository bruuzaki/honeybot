import aiosqlite
import asyncio
import os

DB_PATH = os.path.join(os.environ.get("DB_PATH", "/app/data/honeybot.db"))

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            registered_at TEXT
        )
        """)
        await db.commit()

async def add_user(chat_id: int, name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (chat_id, name, registered_at) VALUES (?, ?, datetime('now'))",
                         (chat_id, name))
        await db.commit()

async def remove_user(chat_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM users WHERE chat_id = ?", (chat_id,))
        await db.commit()

async def list_users():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT chat_id, name FROM users")
        rows = await cur.fetchall()
        return rows

async def get_all_chat_ids():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT chat_id FROM users")
        rows = await cur.fetchall()
        return [r[0] for r in rows]
