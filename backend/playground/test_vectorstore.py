import asyncio

from app.vectorstore.manager import VectorStoreManager


async def main():
    manager = VectorStoreManager()

    print(await manager.collection_exists())

    await manager.delete_collection()

    print(await manager.collection_exists())


if __name__ == "__main__":
    asyncio.run(main())