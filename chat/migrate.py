import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def migrate():
    engine = create_async_engine(DATABASE_URL)
    print("Connecting to database...")
    async with engine.begin() as conn:
        print("Migrating 'chatmessage' table...")
        # Alter the column to be time-zone aware
        await conn.execute(text("ALTER TABLE chatmessage ALTER COLUMN timestamp TYPE TIMESTAMP WITH TIME ZONE USING timestamp AT TIME ZONE 'UTC'"))
        print("Migration complete: 'timestamp' column is now TIMESTAMP WITH TIME ZONE.")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate())
