from sqlmodel import SQLModel
from modules.core.config.database import engine

async def create_tables() -> None:
    print('Creating tables...')
    import modules.core.config.__all_models
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    print('Tables created successfully.')


if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())