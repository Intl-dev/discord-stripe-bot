import aiosqlite
import asyncio

async def create_table():
    db = await aiosqlite.connect("database.db")
    await db.executescript("""
                CREATE TABLE IF NOT EXISTS profiles (
                    profile_name TEXT PRIMARY KEY,
                    discord_id INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS invoices (
                    order_id TEXT PRIMARY KEY,
                    discord_id INTEGER NOT NULL,
                    amount_usd REAL NOT NULL,
                    stripe_url TEXT,
                    status TEXT DEFAULT 'UNPAID'
                )
            """)
    await db.executescript("""
    INSERT INTO invoices (order_id, discord_id, amount_usd, stripe_url)
    VALUES (12345, 123456789, 1, 'fakeurl')
    """)
    await db.commit()
    await db.close()

async def check_unpaid():
    async with aiosqlite.connect("database.db") as db:
        sql = "SELECT discord_id FROM invoices WHERE status != 'PAID'"

        async with db.execute(sql) as cursor:
            rows = await cursor.fetchall()
            users = []
            for row in rows:
                users.append(row[0])

        return users





if __name__ == "__main__":
    asyncio.run(create_table())