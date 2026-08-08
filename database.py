import aiosqlite
import asyncio

async def create_table():
    async with aiosqlite.connect("database.db") as db:
        await db.executescript("""
                CREATE TABLE IF NOT EXISTS profiles (
                    profile_name TEXT PRIMARY KEY,
                    discord_id INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS invoices (
                    order_id TEXT PRIMARY KEY,
                    discord_id INT NOT NULL,
                    amount_usd REAL NOT NULL,
                    stripe_url TEXT,
                    status TEXT DEFAULT 'UNPAID'
                )
            """)
        await db.commit()

async def check_unpaid():
    async with aiosqlite.connect("database.db") as db:
        sql = "SELECT discord_id FROM invoices WHERE status != 'PAID'"

        async with db.execute(sql) as cursor:
            rows = await cursor.fetchall()
            users = []
            for row in rows:
                users.append(row[0])
        return users

async def insert_invoice(order_id, discord_id, amount, payment_url, status):
    """Inserts the invoices gotten from fake-client.py"""
    async with aiosqlite.connect("database.db") as db:
        sql = "SELECT 1 FROM invoices WHERE order_id = ?"
        async with db.execute(sql, (order_id,)) as cursor:
            result = await cursor.fetchone()
        if result is None:
            sql = """
                INSERT INTO invoices (order_id, discord_id, amount_usd, stripe_url, status)
                VALUES (?, ?, ?, ?, ?)
            """
            await db.execute(sql, (order_id, discord_id, amount, payment_url, status))
            await db.commit()
        else:
            print("Order repeated")


if __name__ == "__main__":
    asyncio.run(create_table())