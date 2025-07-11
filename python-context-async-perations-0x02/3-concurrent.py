import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as conn:
        async with conn.execute("SELECT * FROM users WHERE age > 40") as cursor:
            old_users = await cursor.fetchall()
            return old_users

async def fetch_concurrently():
   users,old_users = await asyncio.gather(async_fetch_users(),async_fetch_older_users())
   print(users)
   print(old_users)
    
 
asyncio.run(fetch_concurrently())
