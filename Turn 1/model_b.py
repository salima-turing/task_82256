import asyncio
import aiohttp
import pytest
import aiosqlite


@pytest.mark.asyncio
async def test_async_cloud_api_call():
    async with aiohttp.ClientSession() as session:
        url = 'https://example.com/some/cloud/api/endpoint'
        async with session.get(url) as response:
            data = await response.json()

            assert response.status == 200
            assert 'expected_key' in data

@pytest.mark.asyncio
async def test_database_query():
    async with aiosqlite.connect(':memory:') as db:
        await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        await db.execute("INSERT INTO users (name) VALUES ('AsyncIO User')")

        async with db.execute("SELECT * FROM users") as cursor:
            user = await cursor.fetchone()

            assert user == (1, 'AsyncIO User')
