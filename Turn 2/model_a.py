import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import aiohttp

# Cloud-native application code under test
async def fetch_data_from_api(url: str):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			response.raise_for_status()
			data = await response.json()
			return data

class TestCloudNativeApp(unittest.IsolatedAsyncioTestCase):

	async def test_fetch_data_from_api_success(self):
		expected_data = {"key": "value"}
		mock_response = AsyncMock()
		mock_response.status = 200
		mock_response.json = AsyncMock(return_value=expected_data)

		with patch('aiohttp.ClientSession.get', return_value=mock_response):
			url = "http://example.com/api"
			result = await fetch_data_from_api(url)
			self.assertEqual(result, expected_data)
			mock_response.raise_for_status.assert_awaited_once()
			mock_response.json.assert_awaited_once()

	async def test_fetch_data_from_api_failure(self):
		with patch('aiohttp.ClientSession.get') as mock_get:
			mock_get.return_value.raise_for_status.side_effect = aiohttp.ClientResponseError(status=404, request_info=mock_get.return_value.request_info)
			url = "http://example.com/api"
			with self.assertRaises(aiohttp.ClientResponseError) as cm:
				await fetch_data_from_api(url)
			self.assertEqual(cm.exception.status, 404)

if __name__ == '__main__':
	unittest.main()
