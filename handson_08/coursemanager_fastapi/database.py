from sqlalchemy.ext.asyncio import AsyncSession

async def get_db():
    async with SessionLocal() as session:
        yield session