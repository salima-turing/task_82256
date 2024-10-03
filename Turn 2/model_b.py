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
    """Test class for cloud-native application using AsyncIO."""

    async def test_fetch_data_from_api_success(self):
        """Test successful data fetching from the API."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"key": "value"})

        # Corrected usage of patch decorator
        with patch('aiohttp.ClientSession.get', return_value=mock_response):
            url = "http://example.com/api"
            result = await fetch_data_from_api(url)

        self.assertEqual(result, {"key": "value"})
        mock_response.json.assert_awaited_once()

    async def test_fetch_data_from_api_client_error(self):
        """Test handling of aiohttp.ClientError exception."""
        with patch('aiohttp.ClientSession.get', side_effect=aiohttp.ClientError):
            url = "http://example.com/api"
            with self.assertRaises(aiohttp.ClientError):
                await fetch_data_from_api(url)

    async def test_fetch_data_from_api_status_code_error(self):
        """Test handling of non-200 HTTP status code."""
        mock_response = AsyncMock()
        mock_response.status = 404

        with patch('aiohttp.ClientSession.get', return_value=mock_response):
            url = "http://example.com/api"
            with self.assertRaises(aiohttp.ClientResponseError):
                await fetch_data_from_api(url)


if __name__ == '__main__':
    unittest.main()
